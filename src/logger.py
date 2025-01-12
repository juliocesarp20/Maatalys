import logging
from enum import Enum


class LogLevels(str, Enum):
    info = "INFO"
    warn = "WARN"
    error = "ERROR"
    debug = "DEBUG"


LOG_FORMAT_DEBUG = "%(levelname)s:%(message)s: %(pathname)s:%(funcName)s:%(lineno)d"


def configure_logging(log_level: str = "ERROR"):
    log_level = log_level.upper()
    log_levels = {level.value for level in LogLevels}

    if log_level not in log_levels:
        logging.basicConfig(level=logging.ERROR)
        return

    if log_level == LogLevels.debug.value:
        logging.basicConfig(level=logging.DEBUG, format=LOG_FORMAT_DEBUG)
        return

    logging.basicConfig(level=getattr(logging, log_level))
