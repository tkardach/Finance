import unittest
import tests
from finance.server import app

class TestServer(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()
  
  def tearDown(self):
    pass

  def test_login_path(self):
    pass