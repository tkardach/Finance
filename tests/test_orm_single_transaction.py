import unittest
import tests
from finance.database.account import *
from finance.database.user import *
from finance.database.transactions import *
from finance.database.models import Account, User, SingleTransaction, Role
from finance.database.database import engine, SessionLocal
from datetime import date, timedelta

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
    test_date_1 = date.today() + timedelta(days=1)
    test_date_2 = date.today() + timedelta(days=2)
    test_amount_1 = 500
    test_amount_2 = -200

    def delete_all_rows(self):
        self.session.query(SingleTransaction).delete()
        self.session.query(Account).delete()
        self.session.query(Role).delete()
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
        self.assertEqual(self.test_account_1.single_transactions.count(), 1)
        self.assertEqual(self.test_account_2.single_transactions.count(), 0)
        self.assertEqual(trans.account, self.test_account_1)
        self.assertEqual(trans.name, self.test_transaction_1)
        self.assertEqual(trans.date.date(), self.test_date_1)
        self.assertEqual(trans.amount, self.test_amount_1)
        self.assertEqual(self.test_account_1.single_transactions[0], trans)


    def test_get_all_single_transactions_on_date(self):
        raises = False
        try:
            create_single_transaction(
                account=self.test_account_1,
                name=self.test_transaction_1,
                date=self.test_date_1,
                amount=self.test_amount_1
            )
            create_single_transaction(
                account=self.test_account_1,
                name=self.test_transaction_1,
                date=self.test_date_2,
                amount=self.test_amount_2
            )
            self.session.commit()
            transactions_1 = get_all_single_transactions_on_date(
                self.test_account_1,
                self.test_date_1
            )
            transactions_2 = get_all_single_transactions_on_date(
                self.test_account_1,
                self.test_date_2
            )
            transactions_3 = get_all_single_transactions_on_date(
                self.test_account_2,
                self.test_date_2
            )
        except:
            raises = True
            
        self.assertFalse(raises)
        self.assertEqual(self.test_account_1.single_transactions.count(), 2)
        self.assertEqual(len(transactions_1), 1)
        self.assertEqual(len(transactions_2), 2)
        self.assertEqual(len(transactions_3), 0)


    def test_get_single_transaction_sum_on_date(self):
        raises = False
        try:
            create_single_transaction(
                account=self.test_account_1,
                name=self.test_transaction_1,
                date=self.test_date_1,
                amount=self.test_amount_1
            )
            create_single_transaction(
                account=self.test_account_1,
                name=self.test_transaction_1,
                date=self.test_date_2,
                amount=self.test_amount_2
            )
            self.session.commit()
            sum_1 = get_single_transaction_sum_on_date(
                self.test_account_1,
                self.test_date_1
            )
            sum_2 = get_single_transaction_sum_on_date(
                self.test_account_1,
                self.test_date_2
            )
            sum_3 = get_single_transaction_sum_on_date(
                self.test_account_2,
                self.test_date_1
            )
            expected_sum_1 = self.test_amount_1
            expected_sum_2 = self.test_amount_1 + self.test_amount_2
            expected_sum_3 = 0
        except:
            raises = True
            
        self.assertFalse(raises)
        self.assertEqual(self.test_account_1.single_transactions.count(), 2)
        self.assertEqual(sum_1, expected_sum_1)
        self.assertEqual(sum_2, expected_sum_2)
        self.assertEqual(sum_3, expected_sum_3)