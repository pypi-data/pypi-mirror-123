import sys
import logging
from jinja2 import Environment

logger = logging.getLogger(__name__)

jinja_env = Environment()


def jinja_minify(jinja, settings: dict):
    """Minify jinja main function. Does not minify, rather detects errors (lint)"""
    try:
        jinja_env.parse(jinja)
    except Exception as e:
        logger.error("Jinja validator: {e}")
    return jinja.strip(), None


class Handler:
    """jinja2 handler class"""

    def __init__(self, settings: dict):
        self.settings = settings

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["jinja", "jinja2", "j2"]

    @classmethod
    def name(self):
        return "jinja"

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            # TODO: Implement
            return raw, None
        elif "minify" == mode:
            return jinja_minify(raw, self.settings)
        else:
            logger.warning(f"Unsupported mode '{mode}' for {self.name()} handler, skipping...")
            return raw, None
