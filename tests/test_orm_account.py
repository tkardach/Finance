import unittest
import tests
from finance.database.database import engine, SessionLocal
from finance.database.models import Account, User
from finance.database.user import *
from finance.database.account import *


class TestORMAccount(unittest.TestCase):
    session = None
    test_email = 'test@email.com'
    test_password = 'mytestpassword'
    test_account_name = 'test_account'
    test_balance = 100.50
    test_user = None

    def delete_all_rows(self):
        self.session.query(Account).delete()
        self.session.query(User).delete()
        self.session.commit()


    def setUp(self):
        self.session = SessionLocal()
        self.delete_all_rows()
        self.test_user = create_user(
            self.session, self.test_email, self.test_password)
        create_user(self.session, 'test_email_2@email.com', self.test_password)
        self.session.commit()


    def tearDown(self):
        self.delete_all_rows()
        self.session.close()


    def test_create_account(self):
        raises = False
        try:
            account = create_account(
                self.test_account_name, self.test_user, self.test_balance)
            self.session.commit()
        except:
            self.session.rollback()
            raises = True

        self.assertFalse(raises)
        self.assertEqual(account.name, self.test_account_name)
        self.assertEqual(account.balance, self.test_balance)
        self.assertEqual(len(self.session.query(Account).all()), 1)
        self.assertEqual(self.test_user.accounts.count(), 1)
        self.assertEqual(account, self.test_user.accounts[0])


    def test_get_accounts(self):
        raises = False
        try:
            account1 = create_account(
                self.test_account_name, self.test_user, self.test_balance)
            account2 = create_account(
                'test_account_2', self.test_user, self.test_balance)
            self.session.commit()
            accounts = get_accounts(self.session)
        except:
            self.session.rollback()
            raises = True

        self.assertFalse(raises)
        self.assertEqual(len(accounts), 2)
        self.assertTrue(account1 in accounts)
        self.assertTrue(account2 in accounts)

    def test_get_user_account_by_id(self):
        raises = False
        try:
            account1 = create_account(
                self.test_account_name, self.test_user, self.test_balance)
            self.session.commit()

            account = get_user_account_by_id(account1.account_id, self.test_user)
        except:
            self.session.rollback()
            raises = True
        self.assertFalse(raises)
        self.assertEqual(account1, account)
        