import unittest
import tests
import finance.utility.security as sec

class TestHash(unittest.TestCase):
  def setUp(self):
    pass
  
  def tearDown(self):
    pass

  def test_get_hashed_string(self):
    start_str = 'startingString'
    hashed = sec.get_hashed_string(start_str)
    self.assertNotEqual(start_str, hashed)

    
  def test_check_hashed_string(self):
    start_str = 'startingString'
    hashed = sec.get_hashed_string(start_str)
    self.assertTrue(sec.check_hashed_string(start_str, hashed))