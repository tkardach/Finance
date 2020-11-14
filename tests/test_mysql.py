import os

# Setup env variables used in testing
os.environ['TEST_FLAG'] = 'True'

import unittest
from finance.config import Config
from finance.mysql import *

class TestMySQL(unittest.TestCase):
    def setUp(self):
      pass
    
    def tearDown(self):
      pass

    def test_mysql_login(self):
      raises = False
      try:
        cnx = get_connection()
      except:
        raises = True
      else:
        cnx.close()
      self.assertFalse(raises)