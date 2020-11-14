from configparser import ConfigParser
import os

parser = ConfigParser(os.environ)
parser.read('config.ini')
print(parser['DEFAULT']['db_user'])