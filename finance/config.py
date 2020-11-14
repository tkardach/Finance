import os
from configparser import ConfigParser, BasicInterpolation


# Checks if code is being run from unittest
SECTION = 'default' if not os.environ.get('TEST_FLAG') else 'test'
os.environ['test_var'] = TEST_VAR = 'test'

# Class allows environment variables within config.ini
class EnvInterpolation(BasicInterpolation):
    """Interpolation which expands environment variables in values."""

    def before_get(self, parser, section, option, value, defaults):
        value = super().before_get(parser, section, option, value, defaults)
        return os.path.expandvars(value)

parser = ConfigParser(interpolation=EnvInterpolation())
parser.read('finance/config.ini')

# Config class contains static properties describing system configuration settings
class Config():
  test_env = SECTION == 'test'
  test_var = parser.get(SECTION, 'test_var')
  db_user = parser.get(SECTION, 'db_user')
  db_pass = parser.get(SECTION, 'db_pass')
  db_host = parser.get(SECTION, 'db_host')
  db_name = parser.get(SECTION, 'db_name')
