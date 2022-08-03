import logging
import logging.config
import os
from pathlib import Path

# Ensure logging directory/file are present
logdir = Path().resolve() / "logs"
os.makedirs(str(logdir), exist_ok=True)

# Specifying logging configuration in dictionary format - other formats like python or a logging.conf file 

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "level": "INFO",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "format": "[%(asctime)s %(filename)s %(lineno)d %(levelname)s]: %(message)s",
        },
        "json": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "%(asctime)s %(name)s %(levelname)s %(message)s %(filename)s %(lineno)d %(module)s %(process)d %(thread)d",
        },
        "json_exception": {
            "()": "pythonjsonlogger.jsonlogger.JsonFormatter",
            "format": "[%(asctime)s] %(name)s %(levelname)s %(message)s %(filename)s %(lineno)d %(module)s %(process)d %(thread)d %(exc_info)s",
        },
    },
    "filters": {
        "exclude_error_level": {
            "()": "test_logger.ExcludeLogLevelFilter",
            "level_name": "ERROR",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": f"{logdir}/development.log",
            "formatter": "simple",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "console_json_formatter": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "filters": ["exclude_error_level"],
        },
        "console_exception_json_formatter": {
            "level": "ERROR",
            "class": "logging.StreamHandler",
            "formatter": "json_exception",
        },
    },
    "loggers": {
        "simple_logger": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "detailed_logger": {
            "handlers": ["console_json_formatter", "console_exception_json_formatter"],
            "level": os.getenv("LOG_LEVEL", "INFO"),
            "propagate": False,
        },
    },
}

class ExcludeLogLevelFilter(logging.Filter):
    """
    Removes log records that are not of the configured level
    """

    def __init__(self, level_name):
        self.level_name = level_name

    def filter(self, record):
        return record.levelname != self.level_name

def detailed_logging_example():
    logger = logging.getLogger("detailed_logger")
    # If LOG_LEVEL is set to DEBUG, then the below statement will be printed
    logger.debug("Do not print this")
    logger.info("Print this")

def exception_logging_example():
    logger = logging.getLogger("detailed_logger")
    try:
        5 / 0
    except Exception as e:
        # crystal_logger.error("Error Stuff")
        logger.exception("Exception here", extra={"more": "news"})

if __name__ == "__main__":
    # Configure logging
    logging.config.dictConfig(LOGGING_CONFIG)
    detailed_logging_example()
    exception_logging_example()
