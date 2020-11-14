import os

# Setup env variables used in testing
os.environ['TEST_FLAG'] = 'True'

import unittest
from datetime import date, timedelta
from mysql.connector import errorcode
from finance.config import Config
from finance.mysql import *
from finance.profile import *
from finance.account import *
from finance.transactions import *

class TestAccount(unittest.TestCase):
  test_email = 'test@email.com'
  test_account = 'test_account'
  test_trans_name = 'transaction_test'
  test_balance = 100
  test_profile_id = -1
  test_account_id = -1


  def setup(self):
    self.tear_down()
    create_profile(self.test_email, 'testpassword')
    self.test_profile_id = get_profile_id(self.test_email)
    create_account(self.test_profile_id, self.test_account, self.test_balance)
    self.test_account_id = get_account_id(
      profile_id=self.test_profile_id,
      name=self.test_account)


  def tear_down(self):
    # delete all created profiles
    cnx = get_connection()

    cursor = cnx.cursor()
    cursor.execute('DELETE FROM single_transaction')
    cursor.execute('DELETE FROM account')
    cursor.execute('DELETE FROM profile')
    cnx.commit()

    cursor.close()
    cnx.close()


  def setUp(self):
    self.setup()
  

  def tearDown(self):
    self.tear_down()

  
  def test_create_single_transaction(self):
    add_balance = 50
    create_single_transaction(
      self.test_account_id,
      self.test_trans_name,
      date.today() + timedelta(days=1),
      add_balance)
      
    transactions = get_all_single_transactions_for_account(
      self.test_account_id)

    self.assertEqual(len(transactions), 1)

  
  def test_get_all_single_transactions_for_account(self):
    add_balance = 50
    create_single_transaction(
      self.test_account_id,
      self.test_trans_name,
      date.today() + timedelta(days=1),
      add_balance)
    create_single_transaction(
      self.test_account_id,
      "second_trans_name",
      date.today() + timedelta(days=2),
      add_balance)
      
    transactions = get_all_single_transactions_for_account(
      self.test_account_id)

    self.assertEqual(len(transactions), 2)

  
  def test_get_single_transaction_sum_from_date(self):
    tomorrow = date.today() + timedelta(days=1)
    two_days = date.today() + timedelta(days=2)
    add_balance = 50
    create_single_transaction(
      self.test_account_id,
      self.test_trans_name,
      tomorrow,
      add_balance)
    create_single_transaction(
      self.test_account_id,
      "second_trans_name",
      two_days,
      add_balance)
      
    amount = get_single_transaction_sum_from_date(
      self.test_account_id,
      tomorrow)

    self.assertEqual(amount, add_balance)

    amount = get_single_transaction_sum_from_date(
      self.test_account_id,
      two_days)
    self.assertEqual(amount, add_balance * 2)

  
  def test_get_all_single_transactions_for_account_from_date(self):
    tomorrow = date.today() + timedelta(days=1)
    two_days = date.today() + timedelta(days=2)
    add_balance = 50
    create_single_transaction(
      self.test_account_id,
      self.test_trans_name,
      tomorrow,
      add_balance)
    create_single_transaction(
      self.test_account_id,
      "second_trans_name",
      two_days,
      add_balance)
      
    transactions = get_all_single_transactions_for_account_from_date(
      self.test_account_id,
      tomorrow)

    self.assertEqual(len(transactions), 1)
    

  def test_get_account_balance_for_date(self):
    add_balance = 50
    create_single_transaction(
      self.test_account_id,
      self.test_trans_name,
      date.today() + timedelta(days=1),
      add_balance)
    
    new_balance = get_account_balance_for_date(
      self.test_profile_id,
      self.test_account,
      date.today() + timedelta(days=2)
    )
    self.assertEqual(new_balance, self.test_balance + add_balance)
