import unittest
import tests
import json
from finance.database.database import SessionLocal
from finance.server import app
from finance.database.user import create_user
from finance.database.account import create_account
from finance.database.models import User, Account


class TestRouteAccount(unittest.TestCase):
    test_email = 'test@user.com'
    test_pass = 'test_password'
    test_user = None
    session = None

    def create_account(self, name: str, balance: float):
        account = create_account(
            self.session, name=name, user=self.test_user, balance=balance)
        self.session.commit()

    def create_test_user(self):
        self.test_user = create_user(
            session=self.session, email=self.test_email, password=self.test_pass)
        self.session.commit()

    def get_accounts(self):
        return self.client.get('/accounts')

    def post_login(self, email: str, password: str):
        test_login = {
            'email': email,
            'password': password
        }
        return self.client.post(
            '/login',
            data=json.dumps(test_login),
            content_type='application/json')

    def get_logout(self):
        return self.client.get('/logout')

    def delete_all_rows(self):
        self.session.query(Account).delete()
        self.session.query(User).delete()
        self.session.commit()

    def setUp(self):
        self.session = SessionLocal()
        self.delete_all_rows()
        self.create_test_user()
        self.client = app.test_client()
        self.post_login(self.test_email, self.test_pass)

    def tearDown(self):
        self.delete_all_rows()
        self.session.close()

    def test_get_accounts_empty(self):
        response = self.get_accounts()

        accounts = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(accounts), 0)

    def test_get_accounts(self):
        account_name = 'test_account'
        balance = 95.50
        self.create_account(account_name, balance)
        response = self.get_accounts()

        accounts = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(accounts), 1)
