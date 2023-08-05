import pprint

from jsbeautifier.javascript.options import BeautifierOptions
from jsbeautifier.javascript.beautifier import Beautifier

import esprima

from .jscodegen import CodeGenerator
from .obfuscator import obfuscate

import logging

logger = logging.getLogger(__name__)


generator = CodeGenerator(indent=2)

beautifier = Beautifier()
beautifier_opts = BeautifierOptions()


def js2ast(js: str, name: str = ""):
    ret = {}
    # Trivial reject, parser does not handle empty input
    if len(js.strip()) <= 0:
        logger.warn("Empty input, skipping parsing")
        return ret
    options = {"tolerant": True, "comment": True}
    # parser = esprima.esprima.Parser(js, options=options, delegate=None)

    # ret = parser.parseScript()
    try:
        ret = esprima.parseScript(js, options=options).toDict()
    except esprima.error_handler.Error as e:
        logger.exception("ESPRIMA PARSING FAILED: {e}")
    if "errors" in ret:
        for e in ret.get("errors"):
            logger.error(f"ESPRIMA PARSING ERROR: {e}")
    # logger.info("JS2AST --------------------------")
    # logger.info(pprint.pformat(ret))
    return ret


def ast2js(ast: dict, name: str = ""):
    if not ast:
        logger.warn("Empty input, skipping generation")
        return ""
    ret = generator.generate(ast, name)
    # logger.info("AST2JS --------------------------")
    # logger.info(pprint.pformat(ret))
    return ret


def beautify(js: str, name: str = ""):
    # ret = beautifier.beautify(js, beautifier_opts)
    # ret = dummy_js
    ret = js
    # logger.info(f"SOURCE ({name})--------------------------")
    # logger.info(pprint.pformat(ret))
    return ret


class Handler:
    """JS handler class"""

    def __init__(self, settings: dict):
        self.settings = settings

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["js"]

    @classmethod
    def name(self):
        return "js"

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            js = beautify(raw, name)
            # logger.info(f"returning beautified {js}")
            return js, None
        elif "minify" == mode:
            # js = ast2js(js2ast(beautify(raw, name),name),name)
            js = raw
            return js, None
        else:
            logger.warning(f"Unsupported mode '{mode}' for {self.name()} handler, skipping...")
            return raw, None
