import unittest
from finance.database.account import *
from finance.database.user import *
from finance.database.transactions import *
from finance.database.models import Account, User, SingleTransaction
from finance.database.database import engine, SessionLocal
from datetime import date, datetime, timedelta

class TestORMSingleTransactions(unittest.TestCase):
    session = None
    #User info
    test_email = 'test@email.com'
    test_email_2 = 'test@email2.com'
    test_password = 'mytestpassword'
    test_user = None
    test_user_2 = None

    #Account Info
    test_account_name = 'test_account'
    test_balance_1 = 100.50
    test_balance_2 = 205.85
    test_account_1 = None
    test_account_2 = None

    #Transaction Info
    test_transaction_1 = 'account_1_trans'
    test_transaction_2 = 'account_2_trans'
    test_date_1 = datetime.today() + timedelta(days=1)
    test_date_2 = datetime.today() + timedelta(days=2)
    test_amount_1 = 500
    test_amount_2 = -200

    def delete_all_rows(self):
        self.session.query(SingleTransaction).delete()
        self.session.query(Account).delete()
        self.session.query(User).delete()
        self.session.commit()

    def setUp(self):
        self.session = SessionLocal()
        self.delete_all_rows()
        self.test_user = create_user(
            self.session, self.test_email, self.test_password)
        self.test_user_2 = create_user(
            self.session, self.test_email_2, self.test_password)
        self.test_account_1 = create_account(
            self.test_account_name, self.test_user, self.test_balance_1)
        self.test_account_2 = create_account(
            self.test_account_name, self.test_user_2, self.test_balance_2)
        self.session.commit()

    def tearDown(self):
        self.delete_all_rows()
        self.session.close()


    def test_create_single_transaction(self):
        raises = False
        try:
            trans = create_single_transaction(
                account=self.test_account_1,
                name=self.test_transaction_1,
                date=self.test_date_1,
                amount=self.test_amount_1
            )
            self.session.commit()
        except:
            raises = True

        self.assertFalse(raises)
        self.assertEqual(len(self.session.query(SingleTransaction).all()), 1)
        self.assertEqual(len(self.test_account_1.single_transactions), 1)
        self.assertEqual(len(self.test_account_2.single_transactions), 0)
        self.assertEqual(trans.account, self.test_account_1)
        self.assertEqual(trans.name, self.test_transaction_1)
        self.assertEqual(trans.date.date(), self.test_date_1.date())
        self.assertEqual(trans.amount, self.test_amount_1)
        self.assertEqual(self.test_account_1.single_transactions[0], trans)