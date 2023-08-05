# https://engineeringblog.yelp.com/2017/06/making-photos-smaller.html


# import pngquant

import logging

logger = logging.getLogger(__name__)


def png_minify(png, settings: dict):
    """Minify PNG main function."""
    #    pngquant.config()
    #    png=quant_data(self, data=None, dst=None, ndeep=None, ndigits=None, delete=True):
    # TODO: Implement this
    return png, None


class Handler:
    """PNG handler class"""

    def __init__(self, settings: dict):
        self.settings = settings

    @classmethod
    def is_binary(self):
        return True

    @classmethod
    def extensions(self):
        return ["png"]

    @classmethod
    def name(self):
        return "png"

    def process(self, raw: str, name: str = None):
        mode = self.settings.get("mode")
        if "beautify" == mode:
            # TODO: Implement
            return raw, None
        elif "minify" == mode:
            return png_minify(raw, self.settings)
        else:
            logger.warning(f"Unsupported mode '{mode}' for {self.name()} handler, skipping...")
            return raw, None
