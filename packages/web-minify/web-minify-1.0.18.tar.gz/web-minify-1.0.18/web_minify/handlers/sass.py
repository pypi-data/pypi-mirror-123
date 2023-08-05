from .css import css_minify

import logging

logger = logging.getLogger(__name__)

have_sass = False

try:
    import sass

    have_sass = True
except Exception:
    logger.warning("Could not import sass", exc_info=True)
    logger.warning("NOTE: To install sass, please remember to use  use pip install libsass instead of pip install sass")


class Handler:
    """SASS handler class"""

    def __init__(self, settings: dict):
        self.settings = settings

    @classmethod
    def is_binary(self):
        return False

    @classmethod
    def extensions(self):
        return ["sass"]

    @classmethod
    def name(self):
        return "sass"

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            # TODO: Implement
            return raw, None
        elif "minify" == mode:
            return sass_minify(raw, self.settings)
        else:
            logger.warning(f"Unsupported mode '{mode}' for {self.name()} handler, skipping...")
            return raw, None


def sass_minify(scss, settings: dict):
    """Minify SASS main function."""
    if have_sass:
        try:
            css = sass.compile(string=scss)
        except sass.CompileError as ce:
            return (None, [f"SASS {ce}"])
        except Exception as e:
            return (None, [f"Error: Could not process SASS {e}"])
    css, css_errors = css_minify(css=css, settings=settings)
    return css, css_errors
