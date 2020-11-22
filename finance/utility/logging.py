import logging
import logging.config
from .config import Config


LOGGING_CONFIG = {
  'version': 1,
  'formatters': {
    'standard': {
      'format': '%(asctime)s:%(name)s:%(levelname)s:%(message)s',
      'datefmt': '%m/%d/%Y %H:%M:%S'
    },
  },
  'handlers': {
    'console': {
      'class': 'logging.StreamHandler',
      'level': 'DEBUG',
      'formatter': 'standard',
      'stream': 'ext://sys.stdout'
    },
    'exception': {
      'class': 'logging.FileHandler',
      'level': 'ERROR',
      'formatter': 'standard',
      'filename': 'exceptions.log',
      'mode': 'w'
    },
  },
  'loggers': {
    '': {
      'level': 'DEBUG',
      'handlers': ['console', 'exception'],
      'propogate': False
    },
    'test': {
      'level': 'DEBUG',
      'handlers': ['console'],
      'propogate': False
    }
  }
}

logging.config.dictConfig(LOGGING_CONFIG)

logger_type = 'test' if Config.test_env else None

logger = logging.getLogger(logger_type)