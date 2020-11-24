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
      'handlers': ['console'],
      'propagate': False
    },
    'production': {
      'level': 'DEBUG',
      'handlers': ['console', 'exception'],
      'propagate': False
    },
    'test': {
      'level': 'DEBUG',
      'handlers': [],
      'propagate': False
    }
  }
}

logging.config.dictConfig(LOGGING_CONFIG)

logger = logging.getLogger()

if Config.test_env:
    logger.disabled = True
