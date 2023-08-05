#!/usr/bin/env python
import os
import shutil
import difflib
import pprint
import web_minify.processor
from web_minify.files import generate_file_list
from web_minify.handlers import HandlerManager

import logging

logger = logging.getLogger(__name__)

base_path: str = os.path.abspath(os.path.dirname(__file__))

single_input_path: str = os.path.abspath(os.path.join(base_path, "input/js/fk.js"))
input_path: str = os.path.abspath(os.path.join(base_path, "input/"))
output_base_path: str = os.path.abspath(os.path.join(base_path, "output/"))
expected_base_path: str = os.path.abspath(os.path.join(base_path, "expected/"))


try:
    from colorama import Fore, Back, Style, init

    init()
except ImportError:  # fallback so that the imported classes always exist

    class ColorFallback:
        __getattr__ = lambda self, name: ""

    Fore = Back = Style = ColorFallback()


def color_diff(diff):
    for line in diff:
        if line.startswith("+"):
            yield Fore.GREEN + line + Fore.RESET
        elif line.startswith("-"):
            yield Fore.RED + line + Fore.RESET
        elif line.startswith("^"):
            yield Fore.BLUE + line + Fore.RESET
        else:
            yield line


def _test_handlers():
    settings = {"mode": "test", "input": "", "output": "", "verbose": False}
    hm = HandlerManager(settings)
    assert hm is not None
    extensions = hm.get_supported_extensions()
    assert len(extensions) > 0
    for ext in extensions:
        handler = hm.get_handler_by_extension(ext)
        assert handler is not None
        handler.is_binary()
        handler.extensions()
        handler.process("")
    inexistant_h = hm.get_handler_by_extension("inexistant")
    assert inexistant_h is None


def test_regressions_single():
    # fmt:off
    settings = {
        "mode": "minify"
        , "input": single_input_path
        #, "output": output_path
        , "verbose": True
        , "overwrite": True
        , "force": True
        , "dry_run": False
        , "gzip": True
        , "nproc": 100
        #, "disable_type_css": True
        #, "disable_type_html": True
        #, "disable_type_sass": True
        #, "disable_type_png": True
        #, "disable_type_jpeg": True
        #, "disable_type_svg": True
    }
    # fmt:on
    return regressions_work(settings)


def _test_regressions_minify():
    # fmt:off
    settings = {
        "mode": "minify"
        , "input": input_path
        #, "output": output_path
        , "verbose": False
        , "overwrite": True
        , "force": True
        , "dry_run": False
        , "gzip": True
        , "nproc": 100
        #, "disable_type_css": True
        #, "disable_type_html": True
        #, "disable_type_sass": True
        #, "disable_type_png": True
        #, "disable_type_jpeg": True
        #, "disable_type_svg": True
    }
    # fmt:on
    return regressions_work(settings)


def _test_regressions_beautify():
    # fmt:off
    settings = {
        "mode": "beautify"
        , "input": input_path
        #, "output": output_path
        , "verbose": False
        , "overwrite": True
        , "force": True
        , "dry_run": False
        , "gzip": True
        , "nproc": 100
        #, "disable_type_css": True
        #, "disable_type_html": True
        #, "disable_type_sass": True
        #, "disable_type_png": True
        #, "disable_type_jpeg": True
        #, "disable_type_svg": True
    }
    # fmt:on
    return regressions_work(settings)


def _test_regressions_combinations():
    for dry_run in [True, False]:
        for verbose in [True, False]:
            for force in [False, True]:
                for mode in ["minify", "beautify"]:
                    for overwrite in [True, False]:
                        # fmt:off
                        settings = {
                              "input": input_path
                            , "mode": mode
                            , "verbose": verbose
                            , "overwrite": overwrite
                            , "force": force
                            , "dry_run": dry_run
                            , "gzip": True
                            , "nproc": 100
                            #, "disable_type_css": True
                            #, "disable_type_html": True
                            #, "disable_type_sass": True
                            #, "disable_type_png": True
                            #, "disable_type_jpeg": True
                            #, "disable_type_svg": True
                        }
                        # fmt:on
                        logger.info(f" ###### COMBINATION mode={mode}  verbose={verbose}  overwrite={overwrite}  force={force}  dry_run={dry_run}  ######")
                        regressions_work(settings)


def regressions_work(settings):
    settings = settings.copy()
    mode = settings.get("mode", "unknown")
    output_path = os.path.join(output_base_path, mode)
    expected_path = os.path.join(expected_base_path, mode)
    expected_files = generate_file_list(expected_path)

    settings["output"] = output_path

    logger.info(f" ###### REGRESSION mode={mode}  verbose={settings.get('verbose')}  overwrite={settings.get('overwrite')}  force={settings.get('force')}  dry_run={settings.get('dry_run')}  ######")

    def clear_output():
        shutil.rmtree(output_path, ignore_errors=True)

    # 1. Clear old result if any
    # clear_output()
    # 2. Run tool on input

    processor = web_minify.processor.Processor(settings)
    res, msg = processor.sanity_checks()
    if not res:
        logger.warning(msg)
    assert res
    res, msg = processor.process_files()
    if not res:
        logger.warning(msg)
    assert res
    # 3. Compare output with expected
    # output_files = generate_file_list(output_path)
    # logger.warning(pprint.pformat(expected_files))
    # logger.warning(pprint.pformat(output_files))
    # logger.warning(f"expected_path: {expected_path}")
    # logger.warning(f"output_path: {output_path}")
    errors = 0
    for expected_file in expected_files:
        # logger.warning(f"EXPECTED FILE: {expected_file}")
        rel = expected_file[expected_file.startswith(expected_path) and len(expected_path) + 1 :]
        # logger.warning(f"REL: {rel}")
        output_file = os.path.join(output_path, rel)
        # logger.warning(f"OUTPUTY FILE: {output_file}")
        assert os.path.exists(output_file)
        output_is_binary = output_file.endswith((".png", ".jpeg", ".jpg"))
        expected_is_binary = expected_file.endswith((".png", ".jpeg", ".jpg"))
        output_content = ""
        with open(output_file, "rb") if output_is_binary else open(output_file, "r", encoding="utf-8") as output_handle:
            output_content = output_handle.read()
        expected_content = ""
        with open(expected_file, "rb") if expected_is_binary else open(expected_file, "r", encoding="utf-8") as expected_handle:
            expected_content = expected_handle.read()
        if output_content != expected_content:
            logger.warning(f"--- Output did not match expected for {rel}:")
            diff = difflib.ndiff(output_content.splitlines(1), expected_content.splitlines(1))
            diff = color_diff(diff)
            logger.error("\n".join(diff))
            errors += 1
    assert errors == 0

    # 4. Clear result
    # clear_output()
