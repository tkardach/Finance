import unittest
import tests
from finance.shared import Validation

class TestValidation(unittest.TestCase):
  def setUp(self):
    pass
  
  def tearDown(self):
    pass

  def test_email_validate(self):
      self.assertTrue(Validation.validate_email('test@email.com'))
      self.assertTrue(Validation.validate_email('test@email.gov'))
      self.assertTrue(Validation.validate_email('test@email.eu'))
      self.assertFalse(Validation.validate_email('test@email.c'))
      self.assertFalse(Validation.validate_email('test@email,com'))
      self.assertFalse(Validation.validate_email('test@,email.com'))
      self.assertFalse(Validation.validate_email('email.com'))
