import logging
import logging.config
logging.getLogger("pymongo").setLevel(logging.WARNING)

def setup_logging():
    """
    Set up logging configuration for the application.
    """
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": LOG_FORMAT,
            },
            "detailed": {
                "format": "%(asctime)s - %(name)s - %(levelname)s - %(module)s - %(message)s",
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "level": "DEBUG",
            },
        },
        "root": {
            "handlers": ["console"],
            "level": "DEBUG",
        },
    }

    # Configure logging
    logging.config.dictConfig(logging_config)