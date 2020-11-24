import unittest
import tests
import json
from finance.database.database import SessionLocal
from finance.server import app
from finance.database.user import create_user
from finance.database.account import create_account
from finance.database.transactions import create_recurring_transaction, create_single_transaction
from finance.database.models import User, Account, SingleTransaction, RecurringTransaction
from finance.shared import Timespan
from datetime import date, timedelta
from uuid import uuid4


class TestRouteAccount(unittest.TestCase):
    test_email = 'test@user.com'
    test_pass = 'test_password'
    test_user = None
    session = None

    def create_account(self, name: str, balance: float):
        account = create_account(
            name=name, user=self.test_user, balance=balance)
        self.session.commit()
        return account

    def create_test_user(self):
        self.test_user = create_user(
            session=self.session, email=self.test_email, password=self.test_pass)
        self.session.commit()

    def get_accounts(self):
        return self.client.get('/accounts')

    def post_create_account(self, name, balance):
        data = {
            'name': name,
            'balance': balance
        }
        return self.client.post(
            '/accounts',
            data=json.dumps(data),
            mimetype='application/json')

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

    def get_account(self, account_id):
        return self.client.get('/account/%s' % account_id)

    def get_account_balance(self, account_id, date):
        return self.client.get('/account/%s/balance/%s' % (account_id, date))

    def delete_all_rows(self):
        self.session.query(SingleTransaction).delete()
        self.session.query(RecurringTransaction).delete()
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

    def test_create_account(self):
        account_name = 'test_account'
        balance = 95.50

        response = self.post_create_account(account_name, balance)

        self.assertEqual(response.status_code, 200)

        account = json.loads(response.data)
        self.assertEqual(account['name'], account_name)
        self.assertEqual(account['balance'], balance)

        response = self.get_accounts()

        accounts = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(accounts), 1)

    def test_create_account_400_missing_name(self):
        balance = 95.50

        data = {
            'balance': balance
        }
        return self.client.post(
            '/accounts',
            data=json.dumps(data),
            mimetype='application/json')

        self.assertEqual(response.status_code, 400)

    def test_create_account_400_missing_balance(self):
        data = {
            'name': 'test_name'
        }
        return self.client.post(
            '/accounts',
            data=json.dumps(data),
            mimetype='application/json')

        self.assertEqual(response.status_code, 400)

    def test_get_account(self):
        name = 'test_name'
        balance = 50.65
        account = self.create_account(name, balance)

        response = self.get_account(account.account_id)

        self.assertEqual(response.status_code, 200)

        account_dict = json.loads(response.data)
        self.assertEqual(account_dict['name'], name)
        self.assertEqual(account_dict['balance'], balance)

    def test_get_account_404_path_not_found(self):
        response = self.get_account('not_a_uuid')

        self.assertEqual(response.status_code, 404)

    def test_get_account_404_account_not_found(self):
        response = self.get_account(uuid4())

        self.assertEqual(response.status_code, 404)

    def test_get_account_balance(self):
        name = 'test_name'
        balance = 50.65
        account = self.create_account(name, balance)
        today = date.today()

        response = self.get_account_balance(account.account_id, today)

        self.assertEqual(response.status_code, 200)

        account_dict = json.loads(response.data)
        self.assertEqual(account_dict['balance'], balance)

    def test_get_account_balance_404_path_not_found(self):
        today = date.today()

        response = self.get_account_balance('not_uuid', today)

        self.assertEqual(response.status_code, 404)

    def test_get_account_balance_404_account_not_found(self):
        today = date.today()

        response = self.get_account_balance(uuid4(), today)

        self.assertEqual(response.status_code, 404)

    def test_get_account_balance_with_transactions(self):
        name = 'test_name'
        balance = 50.65
        account = self.create_account(name, balance)

        single = 'test_single'
        single_amount = 100.75
        single_date = date.today() + timedelta(days=14)
        create_single_transaction(
            account, single, single_date, single_amount)
        self.session.commit()

        recurring = 'test_recurring'
        recurring_amount = 50.50
        recurring_date = date.today()
        recurring_timespan = Timespan(0, 2, 0, 0)
        create_recurring_transaction(
            account, recurring, recurring_date, recurring_timespan, recurring_amount)
        self.session.commit()

        one_week = date.today() + timedelta(days=7)
        four_weeks = date.today() + timedelta(days=28)

        first_expected = float(account.balance) + recurring_amount
        second_expected = float(account.balance) + single_amount + (recurring_amount * 3)

        response_first = self.get_account_balance(account.account_id, one_week)
        self.assertEqual(response_first.status_code, 200)

        response_second = self.get_account_balance(account.account_id, four_weeks)
        self.assertEqual(response_second.status_code, 200)

        first_balance = json.loads(response_first.data)
        second_balance = json.loads(response_second.data)
        self.assertEqual(first_balance['balance'], first_expected)
        self.assertEqual(second_balance['balance'], second_expected)

    def test_get_account_balance_401_on_not_logged_in(self):
        name = 'test_name'
        balance = 50.65
        account = self.create_account(name, balance)
        today = date.today()

        self.get_logout()
        response = self.get_account_balance(account.account_id, today)

        self.assertEqual(response.status_code, 401)
