from __future__ import unicode_literals
import logging
import logging.config

LOGGING = {
    "version": 1,
    "formatters": {
        "default": {
            "format": '%(asctime)s %(levelname)-5s [%(name)s:%(threadName)s] %(message)s',
            "datefmt": '%Y-%m-%d %H:%M:%S'
        }
    },
    "filters": {},
    "handlers": {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',#'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
        "develop": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "stream": 'ext://sys.stdout',
            "formatter": "default"
        },
        "production": {
            "class": "logging.handlers.RotatingFileHandler",
            "level": "DEBUG",
            "filename": "/tmp/rasp4php.log",
            "formatter": "default",
            "maxBytes": 4096
        }
    },
    "loggers": {
        "rasp4php": {
            "handlers": ["production", "develop"],
            "level": "INFO"
        }
    }
}


# Global logger
logging.config.dictConfig(LOGGING)
logging.raiseExceptions = False
logger = logging.getLogger('rasp4php')