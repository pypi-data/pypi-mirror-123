import os
import pprint
import datetime
import time
import zlib
from .files import path_is_in_path, generate_file_list, determine_file_extension
from .handlers import HandlerManager
from .time import human_delta
from .modes import Mode

now = time.time()

# from multiprocessing import Pool, cpu_count
from pathos.multiprocessing import ProcessingPool as Pool

import logging

logger = logging.getLogger(__name__)

now = datetime.datetime.utcnow().timestamp()

gzip_suffix = ".gz"


def append_and_return(raw, item):
    if type(item) is "list":
        raw.extend(item)
    else:
        raw.append(item)
    return raw


def b2s(b):
    # return "✅" if b else "❌"
    return "☑️" if b else "-"


class Processor:
    def __init__(self, settings: dict):
        self.settings = settings
        self.input = settings.get("input", None)
        self.output = settings.get("output", None)
        self.input_is_dir = self.input and os.path.isdir(self.input)
        self.input_exists = self.input and os.path.exists(self.input)
        self.output_is_dir = self.output and os.path.isdir(self.output)
        self.output_exists = self.output and os.path.exists(self.output)
        self.mode: Mode = Mode(settings.get("mode", "minify"))
        self.format: bool = settings.get("format", False)
        self.overwrite: bool = settings.get("overwrite", False)
        self.on_change: bool = settings.get("on_change", False)
        self.prefix: bool = settings.get("prefix", False)
        self.gzip: bool = settings.get("gzip", False)
        self.hash: bool = settings.get("hash", False)
        self.verbose: bool = settings.get("verbose", False)
        self.force: bool = settings.get("force", False)
        self.dry_run: bool = settings.get("dry_run", False)
        self.nproc: int = settings.get("nproc", 1)

        self.handlers = HandlerManager()
        self.handlers.prepare_handlers(self.settings)

        self.valid_extensions = self.handlers.get_supported_extensions()
        self.handler_names = self.handlers.get_handler_names()

        if self.verbose:
            logger.info("### Settings:")
            logger.info(pprint.pformat(self.settings))
            logger.info("### Handlers:")
            logger.info(pprint.pformat(self.handler_names))
            logger.info("### Valid extensions:")
            logger.info(pprint.pformat(self.valid_extensions))
        self.pool = None

    def sanity_checks(self):
        valid_modes = list(Mode)
        if not self.mode in valid_modes:
            return (False, f"The specified mode {self.mode} was not valid. NOTE: Valid modes are {pprint.pformat(valid_modes)}")
        if not self.input or not self.input_exists:
            return (False, f"The input specified '{self.input}' did not exist. Input must be an existing directory or file")
        if not self.overwrite and self.on_change:
            return (False, f"On-change will not have an effect so long as overwrite is not enabled")
        if not self.output and not self.overwrite and not self.format:
            return (False, f"Only input '{self.input}' was specified. Without a setting for 'output', 'overwrite' and/or 'format' all processing will fail")
        if path_is_in_path(self.input, self.output):
            return (False, f"The output '{self.output}' is a subpath of input '{self.input}'")
        if path_is_in_path(self.output, self.input):
            return (False, f"The input '{self.input}' is a subpath of output '{self.output}'")
        return True, None

    def process_file(self, input_path: str, output_path: str, now=now):
        encoding = "utf-8"
        # fmt:off
        status={
              "gzip": False
            , "copied": False
            , "written": False
            , "binary": False
            , "skipped": False
            , "empty": False
            , "extension": ""
            , "type": ""
        }
        # fmt:on
        messages = []
        if not input_path:
            return False, status, append_and_return(messages, "No input path specified")
        if not output_path:
            return False, status, append_and_return(messages, "No output path specified")
        handler = None
        is_binary = True
        extension, raw_extension = determine_file_extension(input_path)
        status["extension"] = raw_extension
        handler = self.handlers.get_handler_by_extension(extension)
        if handler:
            status["type"] = handler.name()
            is_binary = handler.is_binary()
            status["binary"] = is_binary
        input_mtime = os.path.getmtime(input_path)
        output_mtime = None
        if os.path.isfile(output_path):
            if not self.overwrite:
                return False, status, append_and_return(messages, "Trying to overwrite without overwrite enabled")
            if self.on_change:
                output_mtime = os.path.getmtime(output_path)
                if not self.overwrite and not self.force and (input_mtime == output_mtime):
                    status["skipped"] = True
                    return True, status, append_and_return(messages, "File not changed, skipping")
                elif not self.overwrite and not self.force and (output_mtime > input_mtime):
                    status["skipped"] = True
                    return True, status, append_and_return(messages, f"Destination file newer than input, skipping ({output_mtime} >= {input_mtime})")
        else:
            output_dir = os.path.dirname(output_path)
            if not os.path.isdir(output_dir):
                os.makedirs(name=output_dir, exist_ok=True)
            if not os.path.isdir(output_dir):
                return False, status, append_and_return(messages, "Output directory did not exist or could not be created")
        vip_file = False
        if not extension:
            # Skip well known files with unsupported file extensions
            base_name = os.path.basename(input_path)
            if base_name in ["sitemap.xml", "favicon.ico", "robots.txt"]:
                vip_file = True
            else:
                return False, status, append_and_return(messages, f"Unknown extension '{raw_extension}' for input file")
        elif not handler:
            return False, status, append_and_return(messages, f"Could not find handler for input file with extension {raw_extension}")
        original_content = None
        try:
            with open(input_path, "rb") if is_binary else open(input_path, "r", encoding=encoding) as file:
                original_content = file.read()
        except Exception as err:
            return False, status, append_and_return(messages, f"Could not load data from input file: {err}")
        if not original_content:
            messages = append_and_return(messages, f"Input file was empty")
            status["empty"] = True
        processed_content = None
        handler_errors = None
        handler_name = handler.name() if handler else None
        handler_disabled = handler_name in self.handler_names and self.settings.get(f"disable_type_{handler.name()}", False)
        extension_disabled = extension in self.valid_extensions and self.settings.get(f"disable_suffix_{extension}", False)
        do_copy = handler is None or vip_file or handler_disabled or extension_disabled
        if do_copy:
            # Perform copy
            if self.verbose:
                logger.info(f"Supposed to copy: {input_path} ({raw_extension})")
            processed_content = original_content
            status["copied"] = True
        else:
            # logger.info(f"SUPPOSED TO PROCESS: {input_path} ({extension})")
            _processed_content, handler_errors = handler.process(original_content, input_path)
            processed_content = _processed_content
        # logger.info(f"Content of file {input_path} was of type {type(original_content)} while processed {type(processed_content)}")
        if handler_errors:
            return False, status, append_and_return(messages, handler_errors)
        if None == processed_content:
            messages = append_and_return(messages, f"Processed file was empty")
            status["empty"] = True
        content_changed = original_content != processed_content
        status["changed"] = content_changed
        try:
            if not self.dry_run:
                with open(output_path, "wb") if is_binary else open(output_path, "w", encoding=encoding) as file:
                    written = file.write(processed_content)
                    if written != len(processed_content):
                        return False, status, append_and_return(messages, f"Partially written output ({written} of {len(processed_content)} bytes)")
                    status["written"] = True
        except Exception as err:
            return False, status, append_and_return(messages, f"Could not write data to output file: {err}")
        try:
            if not self.dry_run:
                # If source and destination is identical then there will be no change in time, so in that case we induce it  by using "now"
                final_time = input_mtime if output_path is not input_path else now
                os.utime(output_path, (final_time, final_time))
        except Exception as err:
            return False, status, append_and_return(messages, f"Could not modify date of output file: {err}")
        if self.gzip:
            gzip_path = f"{output_path}{gzip_suffix}"
            try:
                if not self.dry_run and not is_binary:
                    with open(gzip_path, "wb") as gzip_file:
                        gzip_content = zlib.compress(processed_content.encode(encoding), level=9)
                        if self.verbose:
                            logger.info(f"Producing gzip file'{gzip_path}'")
                        gzip_written = gzip_file.write(gzip_content)
                        if gzip_written != len(gzip_content):
                            return False, status, append_and_return(messages, f"Partially written gzip output ({gzip_written} of {len(gzip_content)} bytes)")
                        status["gzip"] = True
            except Exception as err:
                return False, status, append_and_return(messages, f"Could not write gzip data to output file: {err}")
            try:
                if not self.dry_run and status.get("gzip", False):
                    os.utime(gzip_path, (input_mtime, input_mtime))
            except Exception as err:
                return False, status, append_and_return(messages, f"Could not modify date of gzip file: {err}")
        # All went well, go home happy!
        return True, status, messages

    def process_files_list_item_wrapper(self, item):
        input_path = item["input_path"]
        output_path = item["output_path"]
        single_start_time = datetime.datetime.now()
        result = {}
        # success, copied, skipped, message = self.process_file(input_path=input_path, output_path=output_path)
        result["success"], result["status"], result["messages"] = self.process_file(input_path=input_path, output_path=output_path)
        result["status"]["success"] = result.get("success", False)
        result["status"]["failed"] = not result.get("success", False)
        result["input_path"] = input_path
        result["output_path"] = output_path
        result["single_start_time"] = single_start_time
        single_end_time = datetime.datetime.now()
        single_interval = single_end_time - single_start_time
        result["single_end_time"] = single_end_time
        result["single_interval"] = single_interval
        slow = single_interval > datetime.timedelta(seconds=1)
        result["status"]["slow"] = slow
        result["status"]["time"] = single_interval
        if slow:
            result["messages"].extend([f"Processing was slow ({human_delta(result.get('single_interval'))})"])
        return result

    def table_heads(self, table):
        heads = set()
        for row_key, row_value in table.items():
            heads.update(row_value.keys())
        return heads

    def normalize_tabdata(self, table, heads, remove=[]):
        out = []
        for row_key, row_value in table.items():
            row_out = []
            for head in heads:
                if not head in remove:
                    value = row_value.get(head, "")
                row_out.append(value)
            out.append(row_out)
        return out

    def table_widts(self, table, heads=[]):
        num = 0
        for row in table:
            c = len(row)
            num = max(c, num)
        c = len(heads)
        num = max(c, num)
        cols = [0] * num
        for index, col in enumerate(heads):
            l = len(f"{col}")
            m = max(l, cols[index])
            cols[index] = m
        for row in table:
            for index, col in enumerate(row):
                l = len(f"{col}")
                m = max(l, cols[index])
                cols[index] = m
        return cols

    def log_table(self, name, table, remove=[]):
        heads = ["extension", "type", "success", "failed", "written", "changed", "copied", "binary", "gzip", "skipped", "empty", "time", "slow"]
        # self.table_heads(table)
        heads = [head for head in heads if head not in remove]
        norm = self.normalize_tabdata(table, heads)
        widths = self.table_widts(norm, heads)
        fmt = ""
        lt = 0
        for index, head in enumerate(heads):
            l = widths[index]  # len(head)
            lt += l + 3
            fmt += f"| {{:<{l}}} "
        fmt += "|"
        lt += 1
        logger.info("+" + "-" * (lt - 2) + "+")
        logger.info(fmt.format(*heads))
        logger.info("+" + "-" * (lt - 2) + "+")
        for row_value in norm:
            vals = []
            for value in row_value:
                t = type(value)
                if t is datetime.timedelta:
                    value = human_delta(value)
                elif t is bool:
                    value = b2s(value)
                vals.append(value)
            logger.info(fmt.format(*vals))
        logger.info("+" + "-" * (lt - 2) + "+")

    def log_summary(self, summary):
        ft = {"by_extension": ["type"], "by_type": ["extension"]}
        for k, v in ft.items():
            table = summary.get(k, {}.copy())
            logger.info(f"")
            logger.info(f"{k}:")
            self.log_table(k, table, v)
            logger.info(f"")

    def process_files_list(self, files_list):
        start_time = datetime.datetime.now()
        messages = {}
        results = []
        summary = {}
        if self.dry_run:
            logger.info(f"Dry run enabled, changes will NOT be commited to filesystem")
        if self.nproc > 1:
            logger.info(f"Doing multiprocessing on {len(files_list)} files with {self.nproc} cores...")
            with Pool(self.nproc) as pool:
                results = pool.map(self.process_files_list_item_wrapper, files_list)
        else:
            logger.info(f"Doing sequential processing on {len(files_list)} files...")
            for item in files_list:
                result = self.process_files_list_item_wrapper(item)
                results.append(result)
        logger.info(f"\nDONE!\n")
        # Summarize results
        by_extension = {}
        by_type = {}
        no_time = datetime.timedelta(seconds=0)
        # fmt:off
        order=[
            "extension"
          , "type"
          , "success"
          , 'failed'
          , "copied"
          , "written"
          , "changed"
          , "skipped"
          , "empty"
          , "binary"
          , "gzip"
          , "slow"
          , "time"
        ]
        def_item={
              "extension": ""
            , "type": ""
            , "success": 0
            , "failed": 0
            , "copied": 0
            , "written": 0
            , "changed": 0
            , "skipped": 0
            , "empty": 0
            , "binary": 0
            , "gzip": 0
            , "slow": 0
            , "time": no_time
        }
        time_cols=["time"]
        # fmt:on
        keys = order.copy()
        keys.remove("extension")
        keys.remove("type")
        total = "total"
        by_key = {}
        failed_ct = 0
        sp = " " * 2

        def vertical_header():
            logger.info("")
            stati = ["success", "copied", "written", "changed", "skipped", "empty", "binary", "gzip", "slow"]
            # stati=["success", "gzip"]
            longest = 0
            for s in stati:
                longest = len(s) if len(s) > longest else longest
            r = list(range(longest))
            # logger.info(f"longest={longest}, r={r}")
            for y in r:
                line = ""
                for s in stati:
                    sl = len(s)
                    d = longest - len(s)
                    cond = y >= d
                    # logger.info(f"s={s}, sl={sl}, y={y}, longest={longest}, d={d}, cond={cond}")
                    line += s[y - d] if cond else " "
                    line += sp
                logger.info(line)

        if self.verbose:
            # logger.info(f"Processing '{input_path}' -->[{self.mode.value}]--> '{output_path}'")
            vertical_header()
            fct = 0
            header_interval = 10
            for result in results:
                if fct > header_interval:
                    fct -= header_interval
                    vertical_header()
                s = result.get("status")
                output_path = result.get("output_path")
                logger.info(f"{b2s(s['success'])}{sp}{b2s(s['copied'])}{sp}{b2s(s['written'])}{sp}{b2s(s['changed'])}{sp}{b2s(s['skipped'])}{sp}{b2s(s['empty'])}{sp}{b2s(s['binary'])}{sp}{b2s(s['gzip'])}{sp}{b2s(s['slow'])}{sp}'{output_path}'")
                fct += 1

        for result in results:
            status = result.get("status")
            failed = status.get("failed")
            if failed:
                failed_ct += 1
            extension = status.get("extension") or "?"
            handler_type = status.get("type") or "?"
            extension_item = by_extension.get(extension, def_item.copy())
            type_item = by_type.get(handler_type, def_item.copy())
            for key in keys:
                extension_item["extension"] = extension
                if key in time_cols:
                    extension_item[key] = extension_item.get(key, no_time) + status.get(key, no_time)
                else:
                    extension_item[key] = extension_item.get(key, 0) + (1 if status.get(key, False) else 0)
            for key in keys:
                type_item["type"] = handler_type
                if key in time_cols:
                    type_item[key] = type_item.get(key, no_time) + status.get(key, no_time)
                else:
                    type_item[key] = type_item.get(key, 0) + (1 if status.get(key, False) else 0)

            for key in keys:
                by_key[key] = by_key.get(key, 0) + (1 if status.get(key, False) else 0)

            by_extension[extension] = extension_item
            by_type[handler_type] = type_item

            input_path = f"{result.get('input_path')}"
            for message in result.get("messages"):
                all = messages.get(message, [])
                messages[message] = [*all, input_path]

        for result in results:
            status = result.get("status")
            extension = status.get("extension") or "?"
            handler_type = status.get("type") or "N/A"

            extension_keys = by_key.copy()
            extension_keys["extension"] = total
            by_extension[total] = extension_keys

            type_keys = by_key.copy()
            type_keys["type"] = total
            by_type[total] = type_keys

        summary = {"by_extension": by_extension, "by_type": by_type}
        end_time = datetime.datetime.now()
        interval = end_time - start_time
        if messages:
            logger.warning(f"Messages encountered were:")
            for message, all in messages.items():
                logger.warning(f"{len(all)} x {message}")
                show_count = 5
                count = len(all)
                for index in range(min(show_count, count)):
                    logger.warning(f"    {all[index]}")
                if show_count < count:
                    logger.warning(f"    ... and {count-show_count} more")
                logger.warning("")
        self.log_summary(summary)
        logger.info(f"Performing {self.mode.value} on {len(files_list)} files generated {len(messages)} message(s) and took {human_delta(interval)} total\n")
        if failed_ct > 0:
            logger.error(f"NOTE: {failed_ct} errors occured\n")
        return True

    def _process_existing_dir_to_existing_dir(self):
        input_paths = generate_file_list(self.input, tuple(self.valid_extensions))
        files_list = []
        for input_path in input_paths:
            common = os.path.commonpath((os.path.abspath(self.output), os.path.abspath(input_path)))
            rel = os.path.relpath(os.path.abspath(input_path), os.path.abspath(self.input))
            output_path = os.path.join(os.path.abspath(self.output), rel)
            files_list.append({"input_path": input_path, "output_path": output_path})
        return files_list

    def _process_existing_dir_to_new_dir(self):
        # This is same as _process_existing_dir_to_existing_dir but with a mkdir first
        os.mkdir(self.output)
        self.output_exists = self.output and os.path.exists(self.output)
        return self._process_existing_dir_to_existing_dir()

    def _process_existing_dir_overwrite(self):
        input_paths = generate_file_list(self.input, tuple(self.valid_extensions))
        files_list = []
        for input_path in input_paths:
            files_list.append({"input_path": input_path, "output_path": input_path})
        return files_list

    def _process_existing_file(self):
        files_list = [{"input_path": os.path.abspath(self.input), "output_path": os.path.abspath(self.output)}]
        return files_list

    def _process_existing_file_to_dir(self):
        head, tail = os.path.split(os.path.abspath(self.input))
        files_list = [{"input_path": os.path.abspath(self.input), "output_path": os.path.join(os.path.abspath(self.output), tail)}]
        return files_list

    def process_files(self):
        not_implemented = "not implemented"
        if self.input_is_dir:
            if self.output:
                if self.output_is_dir:
                    files_list = self._process_existing_dir_to_existing_dir()
                    return self.process_files_list(files_list), None
                elif not self.output_exists:
                    files_list = self._process_existing_dir_to_new_dir()
                    return self.process_files_list(files_list), None
                else:
                    return None, f"existing-dir-to-existing-file error"
            elif self.overwrite:
                files_list = self._process_existing_dir_overwrite()
                return self.process_files_list(files_list), None
            elif self.format:
                return None, f"format: {not_implemented}"
            else:
                return None, f"input dir specified without valid output option"
        else:
            if self.output:
                if self.output_is_dir:
                    files_list = self._process_existing_file_to_dir()
                    return self.process_files_list(files_list), None
                elif not self.output_exists:
                    files_list = self._process_existing_file()
                    return self.process_files_list(files_list), None
                else:
                    if self.overwrite:
                        files_list = self._process_existing_file()
                        return self.process_files_list(files_list), None
                    else:
                        return None, f"Cannot overwrite existing file when --overwrite is not enabled"
            elif self.overwrite:
                return None, "overwrite: {not_implemented} 2"
            elif self.format:
                return None, "format: {not_implemented} 2"
            else:
                return None, f"input file specified without valid output option 2"
