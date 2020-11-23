import unittest
import tests
import json
from datetime import date
from finance.database.database import SessionLocal
from finance.server import app
from finance.database.user import create_user
from finance.database.account import create_account
from finance.database.models import User, Account, SingleTransaction, RecurringTransaction
from finance.database.transactions import create_single_transaction, create_recurring_transaction
from finance.shared import Timespan
from dateutil import parser


class TestRouteTransaction(unittest.TestCase):
    test_email = 'test@user.com'
    test_pass = 'test_password'
    test_account_name = 'test_account'
    test_account_id = None
    test_balance = 150.50
    test_user = None
    session = None

    test_trans_name = 'transaction_name'
    test_trans_amount = 50.75
    test_trans_date = date.today()
    test_trans_timespan = Timespan(0, 2, 0, 0)

    def create_account(self):
        self.test_account = create_account(
            name=self.test_account_name, user=self.test_user, balance=self.test_balance)
        self.session.commit()
        self.test_account_id = self.test_account.account_id

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
            'date': date.strftime('%m-%d-%Y'),
            'account_id': account_id
        }
        return self.client.post(
            '/single-transactions',
            data=json.dumps(data),
            mimetype='application/json')

    def get_single_transaction(self, account_id: str):
        return self.client.get('/single-transactions/%s' % account_id)

    def post_create_recurring_transaction(
            self, name: str, amount: float, start_date: date, account_id: str, timespan: Timespan):
        data = {
            'name': name,
            'amount': amount,
            'start_date': start_date.strftime('%m-%d-%Y'),
            'account_id': account_id,
            'timespan': timespan.to_timespan_str()
        }
        return self.client.post(
            '/recurring-transactions',
            data=json.dumps(data),
            mimetype='application/json')

    def get_recurring_transaction(self, account_id: str):
        return self.client.get('/recurring-transactions/%s' % account_id)

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

        trans = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(trans['name'], self.test_trans_name)
        self.assertEqual(trans['amount'], self.test_trans_amount)
        self.assertEqual(parser.parse(
            trans['date']).date(), self.test_trans_date)

    def test_create_single_transaction_404_on_no_account(self):
        response = self.post_create_single_transaction(
            self.test_trans_name, self.test_trans_amount, self.test_trans_date, 'doesnotexist')

        self.assertEqual(response.status_code, 404)

    def test_create_single_transaction_401_on_not_logged_in(self):
        self.get_logout()
        response = self.post_create_single_transaction(
            self.test_trans_name, self.test_trans_amount, self.test_trans_date, self.test_account_id)

        self.assertEqual(response.status_code, 401)

    def test_get_single_transactions(self):
        create_single_transaction(
            account=self.test_account,
            name=self.test_trans_name,
            date=self.test_trans_date,
            amount=self.test_trans_amount
        )
        create_single_transaction(
            account=self.test_account,
            name=self.test_trans_name,
            date=self.test_trans_date,
            amount=self.test_trans_amount
        )
        self.session.commit()
        response = self.get_single_transaction(self.test_account_id)

        self.assertEqual(response.status_code, 200)

        transactions = json.loads(response.data)
        self.assertEqual(len(transactions), 2)

    def test_get_single_transactions_404_on_no_account(self):
        self.session.commit()
        response = self.get_single_transaction('does_not_exist')

        self.assertEqual(response.status_code, 404)

    def test_create_recurring_transaction(self):
        response = self.post_create_recurring_transaction(
            self.test_trans_name, self.test_trans_amount, self.test_trans_date, 
            self.test_account_id, self.test_trans_timespan)

        trans = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(trans['name'], self.test_trans_name)
        self.assertEqual(trans['amount'], self.test_trans_amount)
        self.assertEqual(parser.parse(
            trans['start_date']).date(), self.test_trans_date)
        self.assertEqual(trans['timespan'], self.test_trans_timespan.to_timespan_str())

    def test_create_recurring_transaction_404_on_no_account(self):
        response = self.post_create_recurring_transaction(
            self.test_trans_name, self.test_trans_amount, self.test_trans_date, 
            'doesnotexist', self.test_trans_timespan)

        self.assertEqual(response.status_code, 404)

    def test_create_recurring_transaction_401_on_not_logged_in(self):
        self.get_logout()
        response = self.post_create_recurring_transaction(
            self.test_trans_name, self.test_trans_amount, self.test_trans_date, 
            self.test_account_id, self.test_trans_timespan)

        self.assertEqual(response.status_code, 401)

    def test_create_recurring_transaction_400_on_invalid_timespan(self):
        data = {
            'name': self.test_trans_name,
            'amount': self.test_trans_amount,
            'start_date': self.test_trans_date.strftime('%m-%d-%Y'),
            'account_id': self.test_account_id,
            'timespan': 'invalid'
        }
        response = self.client.post(
            '/recurring-transactions',
            data=json.dumps(data),
            mimetype='application/json')

        self.assertEqual(response.status_code, 400)

    def test_get_single_transactions(self):
        create_recurring_transaction(
            account=self.test_account,
            name=self.test_trans_name, 
            amount=self.test_trans_amount, 
            start_date=self.test_trans_date, 
            timespan=self.test_trans_timespan)
        create_recurring_transaction(
            account=self.test_account,
            name=self.test_trans_name, 
            amount=self.test_trans_amount, 
            start_date=self.test_trans_date, 
            timespan=self.test_trans_timespan)
        self.session.commit()
        
        response = self.get_recurring_transaction(self.test_account_id)

        self.assertEqual(response.status_code, 200)

        transactions = json.loads(response.data)
        self.assertEqual(len(transactions), 2)

    def test_get_single_transactions_404_on_no_account(self):
        self.session.commit()
        response = self.get_recurring_transaction('does_not_exist')

        self.assertEqual(response.status_code, 404)
