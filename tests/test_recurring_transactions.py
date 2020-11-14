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
from finance.shared import *

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
    cursor.execute('DELETE FROM recurring_transaction')
    cursor.execute('DELETE FROM account')
    cursor.execute('DELETE FROM profile')
    cnx.commit()

    cursor.close()
    cnx.close()


  def setUp(self):
    self.setup()
  

  def tearDown(self):
    self.tear_down()


  def test_get_timespan_str(self):
    expected = "12:50:10:1"
    result = Timespan.get_timespan_str(12, 50, 10, 1)
    self.assertEqual(result, expected)
  
  def test_get_timespan(self):
    for d in range(32):
      for w in range(53):
        for m in range(13):
          for y in range(2):
            timespan = Timespan.get_timespan_str(d, w, m, y)
            result = Timespan.get_timespan(timespan)
            self.assertIsNotNone(result)
            self.assertEqual(result.days, d)
            self.assertEqual(result.weeks, w)
            self.assertEqual(result.months, m)
            self.assertEqual(result.years, y)
  

  def test_get_timespan_fail_year(self):
    timespan = Timespan.get_timespan_str(0,0,0,2)
    result = Timespan.get_timespan(timespan)
    self.assertIsNone(result)
    timespan = Timespan.get_timespan_str(0,0,13,0)
    result = Timespan.get_timespan(timespan)
    self.assertIsNone(result)
    timespan = Timespan.get_timespan_str(0,53,0,0)
    result = Timespan.get_timespan(timespan)
    self.assertIsNone(result)
    timespan = Timespan.get_timespan_str(32,0,0,0)
    result = Timespan.get_timespan(timespan)
    self.assertIsNone(result)

    
  def test_create_recurring_transaction(self):
    biweekly = Timespan(0, 2, 0, 0)
    create_recurring_transaction(
      self.test_account_id,
      self.test_trans_name,
      date.today(),
      biweekly,
      100)
    transactions = get_all_recurring_transactions_for_account(self.test_account_id)
    self.assertIsNotNone(transactions)
    self.assertEqual(len(transactions), 1)
    

  def test_get_all_recurring_transactions_for_account(self):
    biweekly = Timespan(0, 2, 0, 0)
    create_recurring_transaction(
      self.test_account_id,
      self.test_trans_name,
      date.today(),
      biweekly,
      100)
      
    create_recurring_transaction(
      self.test_account_id,
      self.test_trans_name,
      date.today(),
      biweekly,
      100)

    transactions = get_all_recurring_transactions_for_account(self.test_account_id)
    self.assertIsNotNone(transactions)
    self.assertEqual(len(transactions), 2)


  def test_get_all_recurring_transactions_for_account_from_date(self):
    biweekly = Timespan(0, 2, 0, 0)
    create_recurring_transaction(
      self.test_account_id,
      self.test_trans_name,
      date.today() + timedelta(days=10),
      biweekly,
      100)
      
    create_recurring_transaction(
      self.test_account_id,
      self.test_trans_name,
      date.today(),
      biweekly,
      100)

    transactions = get_all_recurring_transactions_for_account_from_date(
      self.test_account_id,
      date.today())
    self.assertIsNotNone(transactions)
    self.assertEqual(len(transactions), 1)

    
  def test_get_recurring_transaction_sum_from_date(self):
    biweekly = Timespan(0, 2, 0, 0)
    trans = 100
    create_recurring_transaction(
      self.test_account_id,
      self.test_trans_name,
      date.today(),
      biweekly,
      trans)

    amount = get_recurring_transaction_sum_from_date(
      self.test_account_id,
      date.today() + timedelta(days=28))
    self.assertEqual(amount, trans * 2)

    amount = get_recurring_transaction_sum_from_date(
      self.test_account_id,
      date.today() + timedelta(days=32))
    self.assertEqual(amount, trans * 2)

    new_amount = 50
    create_recurring_transaction(
      self.test_account_id,
      "test_trans_2",
      date.today(),
      Timespan(0, 0, 1, 0),
      new_amount)

    amount = get_recurring_transaction_sum_from_date(
      self.test_account_id,
      date.today() + timedelta(days=32))
    self.assertEqual(amount, trans * 2 + new_amount)
    