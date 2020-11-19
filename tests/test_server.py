import unittest
from finance.server.server import app

class TestServer(unittest.TestCase):
  def setUp(self):
    self.client = app.test_client()
  
  def tearDown(self):
    pass

  def test_login_path(self):
    response = self.client.post(
      '/login',
      data=
    )