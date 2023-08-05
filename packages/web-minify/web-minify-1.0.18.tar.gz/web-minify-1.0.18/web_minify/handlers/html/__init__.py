#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""HTML Minifier functions for CSS-HTML-JS-Minify."""

import re
import logging
from bs4 import BeautifulSoup

from .html import html_minify

logger = logging.getLogger(__name__)


space_re = re.compile(r"^(\s*)", re.MULTILINE)


def html_beautify(raw, settings, encoding=None, formatter="minimal", indents=4):
    s = BeautifulSoup(raw, "html.parser")
    return space_re.sub(r"\1" * indents, s.prettify(encoding=encoding, formatter=formatter)), None


class Handler:
    """HTML handler class"""

    def __init__(self, settings: dict):
        self.settings = settings

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["html", "htm"]

    @classmethod
    def name(self):
        return "html"

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            return html_beautify(raw, self.settings)
        elif "minify" == mode:
            return html_minify(raw, self.settings)
        else:
            logger.warning(f"Unsupported mode '{mode}' for {self.name()} handler, skipping...")
            return raw, None
