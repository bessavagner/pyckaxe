"""
    This module provides the default settings of the
    package test
"""

from importlib import metadata


package = metadata.metadata('pyckaxe')

name = package['name']
version = package['version']
author = package['author']
author_email = package['author-email']
summary = package['summary']

TITLE = name
DELIMITER = len(TITLE)*"="
HEADER = (
    f"{DELIMITER}"
    f"{TITLE}"
    f"Version: {version}"
    f"Description: {summary }"
    f"Authors: {author}"
    f"{DELIMITER}"
)

USER_AGENT = ('Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) '
              'Gecko/20100101 Firefox/112.0')

CONFIG_LOG = {
    "version": 1,
    "formatters": {
        "client": {
            "format": "%(levelname)s: %(message)s"
        },
        "standard": {
            "format": "%(levelname)s - function: (%(name)s at %(funcName)s line %(lineno)d): %(message)s"
        },
        "file": {
            "format": "%(levelname)s - function: (%(name)s at %(funcName)s line %(lineno)d): %(message)s",
            "datefmt": "%y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "client": {
            "class": "logging.StreamHandler",
            "formatter": "client",
            "level": "INFO"
        },
        "standard": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
            "level": "DEBUG"
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "file",
            "level": "DEBUG",
            "filename": "report.log",
            "encoding": "utf8"
        }
    },
    "root": {
        "handlers": [
            "standard"
        ],
        "level": "DEBUG"
    },
    "loggers": {
        "client": {
            "handlers": [
                "client"
            ],
            "level": "DEBUG",
            "propagate": False
        },
        "standard": {
            "handlers": [
                "standard"
            ],
            "level": "DEBUG",
            "propagate": False
        },
        "report": {
            "handlers": [
                "file"
            ],
            "level": "DEBUG",
            "propagate": False
        }
    }
}
