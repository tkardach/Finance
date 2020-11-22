import unittest
import tests
import json
from datetime import date
from finance.database.database import SessionLocal
from finance.server import app
from finance.database.user import create_user
from finance.database.account import create_account
from finance.database.models import User, Account, SingleTransaction, RecurringTransaction


class TestRouteTransaction(unittest.TestCase):
    test_email = 'test@user.com'
    test_pass = 'test_password'
    test_account = 'test_account'
    test_account_id = None
    test_balance = 150.50
    test_user = None
    session = None

    test_trans_name = 'transaction_name'
    test_trans_amount = 50.75
    test_trans_date = date.today()

    def create_account(self):
        account = create_account(
            name=self.test_account, user=self.test_user, balance=self.test_balance)
        self.session.commit()
        self.test_account_id = account.account_id

    def create_test_user(self):
        self.test_user = create_user(
            session=self.session, email=self.test_email, password=self.test_pass)
        self.session.commit()

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

    def post_create_single_transaction(self, name: str, amount: float, date: date, account_id: str):
        data = {
            'name': name,
            'amount': amount,
            'date': date.strftime('%m/%d/%Y'),
            'account_id': account_id
        }
        return self.client.post(
            '/single-transaction',
            data=json.dumps(data),
            mimetype='application/json')

    def delete_all_rows(self):
        self.session.query(RecurringTransaction).delete()
        self.session.query(SingleTransaction).delete()
        self.session.query(Account).delete()
        self.session.query(User).delete()
        self.session.commit()

    def setUp(self):
        self.session = SessionLocal()
        self.delete_all_rows()
        self.create_test_user()
        self.create_account()
        self.client = app.test_client()
        self.post_login(self.test_email, self.test_pass)

    def tearDown(self):
        self.delete_all_rows()
        self.session.close()

    def test_create_single_transaction(self):
        response = self.post_create_single_transaction(
            self.test_trans_name, self.test_trans_amount, self.test_trans_date, self.test_account_id)

        self.assertEqual(response.status_code, 200)

    def test_create_single_transaction_404_on_no_account(self):
        response = self.post_create_single_transaction(
            self.test_trans_name, self.test_trans_amount, self.test_trans_date, 'doesnotexist')

        self.assertEqual(response.status_code, 404)

    def test_create_single_transaction_401_on_not_logged_in(self):
        self.get_logout()
        response = self.post_create_single_transaction(
            self.test_trans_name, self.test_trans_amount, self.test_trans_date, self.test_account_id)

        self.assertEqual(response.status_code, 401)
