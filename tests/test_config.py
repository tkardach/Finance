import os

# Setup env variables used in testing
os.environ['TEST_FLAG'] = 'True'

import unittest
from finance.config import Config, TEST_VAR

class TestConfigurationFile(unittest.TestCase):

    def setUp(self):
      pass
    
    def tearDown(self):
      pass

    def test_mock_configuration(self):
      self.assertTrue(Config.test_env)

    def test_mock_db_user(self):
      self.assertEqual(Config.db_user, 'test')

    def test_mock_env_var(self):
      self.assertEqual(Config.test_var, TEST_VAR)
      
