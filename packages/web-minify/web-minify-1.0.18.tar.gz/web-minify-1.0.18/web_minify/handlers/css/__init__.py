#!/usr/bin/env python3
"""CSS Minifier functions for CSS-HTML-JS-Minify."""

from .variables import EXTENDED_NAMED_COLORS, CSS_PROPS_TEXT
from .css import css_minify

__all__ = ("css_minify", "condense_semicolons")

import logging

logger = logging.getLogger(__name__)


class Handler:
    """CSS handler class"""

    def __init__(self, settings: dict):
        self.settings = settings

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["css"]

    @classmethod
    def name(self):
        return "css"

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            # TODO: Implement
            return raw, None
        elif "minify" == mode:
            return css_minify(raw, self.settings)
        else:
            logger.warning(f"Unsupported mode '{mode}' for {self.name()} handler, skipping...")
            return raw, None
