from io import StringIO

from calmjs.parse import io
from calmjs.parse import rules
from calmjs.parse.exceptions import ECMASyntaxError
from calmjs.parse.lexers.es5 import Lexer
from calmjs.parse.parsers.es5 import parse
from calmjs.parse.unparsers.es5 import Unparser

import logging

logger = logging.getLogger(__name__)


class Crimper:
    def __init__(self, settings):
        self.settings = settings

    def crimp(self, raw, mangle=True, obfuscate=True, indent_width=4, drop_semi=True, encoding="utf-8"):
        enabled_rules = [rules.minify(drop_semi=drop_semi or mangle)]
        if obfuscate or mangle:
            enabled_rules.append(rules.obfuscate(reserved_keywords=Lexer.keywords_dict.keys()))
        # if pretty:
        #    enabled_rules.append(rules.indent(indent_str=' ' * indent_width))
        printer = Unparser(rules=enabled_rules)
        out = raw
        with StringIO(raw) as input_stream:
            with StringIO() as output_stream:
                try:
                    io.write(printer, io.read(parse, input_stream), output_stream)
                except ECMASyntaxError as e:
                    return raw, [f"ECMASyntaxError: {e}"]
                except (IOError, OSError) as e:
                    return raw, [f"IOError: {e}"]
                except UnicodeDecodeError as e:
                    return raw, [f"UnicodeDecodeError (read) error: {e}"]
                except UnicodeEncodeError as e:
                    return raw, [f"UnicodeEncodeError (write) error: {e}"]
                except Exception as e:
                    logger.exception(
                        f"Unknown error: {e}",
                    )
                    return raw, [f"Unknown error: {e}"]
                # no need to close any streams as they are callables and that the io
                # read/write functions take care of that.
                out = output_stream.getvalue()
        return out, None
