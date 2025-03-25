from logging.config import dictConfig

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,

    "formatters": {
        "default": {
            "format": "[%(asctime)s] [%(levelname)s] %(name)s: %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },

    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        # optional: log to the file
        # "file": {
        #     "class": "logging.FileHandler",
        #     "filename": "logs/app.log",
        #     "formatter": "default",
        #     "level": "INFO"
        # }
    },

    "root": {
        "handlers": ["console"],  # можешь добавить "file"
        "level": "INFO",
    },

    "loggers": {
        "uvicorn.error": {
            "level": "INFO",
        },
        "uvicorn.access": {
            "level": "INFO",
        },
    }
}


def setup_logging():
    dictConfig(LOGGING_CONFIG)
