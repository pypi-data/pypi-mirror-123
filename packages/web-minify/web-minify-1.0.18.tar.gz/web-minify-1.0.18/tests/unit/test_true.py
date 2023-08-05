import logging
import datetime
import time
import os

logger = logging.getLogger(__name__)


def test_true():
    logger.info("Dummy unit test")
    return True
