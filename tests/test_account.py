import os

# Setup env variables used in testing
os.environ['TEST_FLAG'] = 'True'

import unittest
from mysql.connector import errorcode
from finance.config import Config
from finance.mysql import *
from finance.profile import *
from finance.account import *

class TestAccount(unittest.TestCase):
  test_email = 'test@email.com'
  test_email_2 = 'test@email2.com'
  test_account = 'test_account'
  test_id = -1
  test_id_2 = -1

  def setup(self):
    self.tear_down()
    create_profile(self.test_email, 'testpassword')
    create_profile(self.test_email_2, 'testpassword')
    self.test_id = get_profile_id(self.test_email)
    self.test_id_2 = get_profile_id(self.test_email_2)
    create_account(self.test_id, self.test_account)
    create_account(self.test_id_2, self.test_account)


  def tear_down(self):
    # delete all created profiles
    cnx = get_connection()

    cursor = cnx.cursor()
    cursor.execute('DELETE FROM account')
    cursor.execute('DELETE FROM profile')
    cnx.commit()

    cursor.close()
    cnx.close()

  def setUp(self):
    self.setup()
  
  def tearDown(self):
    self.tear_down()

  def test_get_accounts(self):
    accounts = get_accounts()
    self.assertIsNotNone(accounts)
    self.assertEqual(len(accounts), 2)

    self.tear_down()
    accounts = get_accounts()
    self.assertIsNotNone(accounts)
    self.assertEqual(len(accounts), 0)

  def test_get_accounts_for_profile(self):
    accounts = get_accounts_for_profile(self.test_id)
    self.assertIsNotNone(accounts)
    self.assertEqual(len(accounts), 1)

  def test_create_account(self):
    accounts = get_accounts_for_profile(self.test_id)
    self.assertIsNotNone(accounts)
    self.assertEqual(len(accounts), 1)

    new_account = 'new_account'
    create_account(self.test_id, new_account)
    accounts = get_accounts_for_profile(self.test_id)
    self.assertIsNotNone(accounts)
    self.assertEqual(len(accounts), 2)

  def test_create_account_duplicate(self):
    accounts = get_accounts_for_profile(self.test_id)
    self.assertIsNotNone(accounts)
    self.assertEqual(len(accounts), 1)

    new_account = 'new_account'
    raises = False
    try:
      create_account(self.test_id, self.test_account)
    except:
      raises = True

    self.assertTrue(raises)

  def test_create_account_fail_on_bad_profile(self):
    raises = False
    try:
      create_account(-1, 'test')
    except:
      raises = True
    self.assertTrue(raises)

  def test_get_account_by_name_and_profile(self):
    account_by_id = get_account_by_name_and_profile(
      self.test_account, 
      self.test_id)
    self.assertIsNotNone(account_by_id)
    self.assertEqual(account_by_id[1], self.test_account)
    self.assertEqual(account_by_id[2], self.test_id)

  def test_get_account_by_name_and_profile_2(self):
    account_by_id = get_account_by_name_and_profile(
      self.test_account, 
      self.test_id_2)
    self.assertIsNotNone(account_by_id)
    self.assertEqual(account_by_id[1], self.test_account)
    self.assertEqual(account_by_id[2], self.test_id_2)

  def test_get_account_by_name_and_profile_bad_profile_id(self):
    account_by_id = get_account_by_name_and_profile(
      self.test_account, 
      -1)
    self.assertIsNone(account_by_id)

  def test_get_account_by_name_and_profile_bad_account_name(self):
    account_by_id = get_account_by_name_and_profile(
      'account_does_not_exist', 
      self.test_id)
    self.assertIsNone(account_by_id)

  def test_get_account_id(self):
    account_id = get_account_id(self.test_account, self.test_id)
    self.assertIsNotNone(account_id)
    
    account = get_account_by_id(account_id)
    self.assertEqual(account_id, account[0])
    self.assertEqual(self.test_account, account[1])
    self.assertEqual(self.test_id, account[2])
