import os
import pkg_resources
from .files import read_file

import logging

logger = logging.getLogger(__name__)

__version__ = None
version_filename = "VERSION"

wm_path: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
wm_version_file = f"{wm_path}/{version_filename}"

places_looked = []

if pkg_resources.resource_exists(__name__, version_filename):
    __version__ = pkg_resources.resource_string(__name__, version_filename).decode("utf-8").strip()

if not __version__ and os.path.exists(wm_version_file):
    __version__ = read_file(wm_version_file)

if not __version__:
    logger.warning(f"No version found in wm_path={wm_path}, wm_version_file={wm_version_file}")
    __version__ = "0.0.0"
