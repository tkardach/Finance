import unittest
import tests
from finance.database.account import *
from finance.database.user import *
from finance.database.transactions import *
from finance.database.models import Account, User, RecurringTransaction, Role
from finance.database.database import engine, SessionLocal
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta


class TestORMRecurringTransactions(unittest.TestCase):
    session = None
    # User info
    test_email = 'test@email.com'
    test_email_2 = 'test@email2.com'
    test_password = 'mytestpassword'
    test_user = None
    test_user_2 = None

    # Account Info
    test_account_name = 'test_account'
    test_balance_1 = 100.50
    test_balance_2 = 205.85
    test_account_1 = None
    test_account_2 = None

    # Transaction Info
    test_transaction_1 = 'account_1_trans'
    test_transaction_2 = 'account_2_trans'
    test_date_1 = date.today() + timedelta(days=1)
    test_date_2 = date.today() + timedelta(days=2)
    test_amount_1 = 500
    test_amount_2 = -200
    test_amount_3 = -1000
    biweekly = Timespan(0, 2, 0, 0)
    monthly = Timespan(0, 0, 1, 0)
    yearly = Timespan(0, 0, 0, 1)

    def delete_all_rows(self):
        self.session.query(RecurringTransaction).delete()
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

    def test_create_recurring_transaction(self):
        raises = False
        try:
            trans = create_recurring_transaction(
                account=self.test_account_1,
                name=self.test_transaction_1,
                start_date=self.test_date_1,
                timespan=self.biweekly,
                amount=self.test_amount_1
            )
            self.session.commit()
        except:
            raises = True

        self.assertFalse(raises)
        self.assertEqual(
            len(self.session.query(RecurringTransaction).all()), 1)
        self.assertEqual(self.test_account_1.recurring_transactions.count(), 1)
        self.assertEqual(self.test_account_2.recurring_transactions.count(), 0)
        self.assertEqual(
            self.test_account_1.recurring_transactions.first(), trans)
        self.assertEqual(trans.account, self.test_account_1)
        self.assertEqual(trans.name, self.test_transaction_1)
        self.assertEqual(trans.start_date.date(), self.test_date_1)
        self.assertEqual(trans.timespan, self.biweekly.to_timespan_str())
        self.assertEqual(trans.amount, self.test_amount_1)

    def test_get_all_recurring_transactions_on_date(self):
        raises = False
        try:
            create_recurring_transaction(
                account=self.test_account_1,
                name=self.test_transaction_1,
                start_date=self.test_date_1,
                timespan=self.biweekly,
                amount=self.test_amount_1
            )
            create_recurring_transaction(
                account=self.test_account_1,
                name=self.test_transaction_1,
                start_date=self.test_date_2,
                timespan=self.biweekly,
                amount=self.test_amount_2
            )
            self.session.commit()
            transactions_1 = get_all_recurring_transactions_on_date(
                self.test_account_1,
                self.test_date_1
            )
            transactions_2 = get_all_recurring_transactions_on_date(
                self.test_account_1,
                self.test_date_2
            )
            transactions_3 = get_all_recurring_transactions_on_date(
                self.test_account_2,
                self.test_date_2
            )
        except:
            raises = True

        self.assertFalse(raises)
        self.assertEqual(self.test_account_1.recurring_transactions.count(), 2)
        self.assertEqual(len(transactions_1), 1)
        self.assertEqual(len(transactions_2), 2)
        self.assertEqual(len(transactions_3), 0)

    def test_get_all_recurring_transactions_on_date(self):
        start_date = date.today()
        raises = False
        try:
            create_recurring_transaction(
                account=self.test_account_1,
                name=self.test_transaction_1,
                start_date=start_date,
                timespan=self.biweekly,
                amount=self.test_amount_1
            )
            create_recurring_transaction(
                account=self.test_account_1,
                name=self.test_transaction_1,
                start_date=start_date,
                timespan=self.monthly,
                amount=self.test_amount_2
            )
            create_recurring_transaction(
                account=self.test_account_1,
                name=self.test_transaction_1,
                start_date=start_date,
                timespan=self.yearly,
                amount=self.test_amount_3
            )
            self.session.commit()

            # recurring transactions charge on the date of creation
            # base_sum is the sum of all transactions for their initial state
            base_sum = self.test_amount_1 + self.test_amount_2 + self.test_amount_3
            # in 3 weeks we expect the biweekly payout to be 1x
            expected_sum_1 = base_sum + self.test_amount_1
            # in 1 month we expect
            #   monthly payout to be 1x
            #   biweekly payout to be 2x
            expected_sum_2 = base_sum + (self.test_amount_1 * 2) + self.test_amount_2
            # in 1 year we expect
            #   monthly payout to be 12x
            #   biweekly payout to be 26
            #   yearly payout to be 1
            expected_sum_3 = base_sum + (self.test_amount_1 * 26) + \
                (self.test_amount_2 * 12) + self.test_amount_3

            date_1 = start_date + relativedelta(weeks=+3)
            date_2 = start_date + relativedelta(months=+1)
            date_3 = start_date + relativedelta(years=+1)
            sum_1 = get_recurring_transaction_sum_on_date(
                self.test_account_1, date_1)
            sum_2 = get_recurring_transaction_sum_on_date(
                self.test_account_1, date_2)
            sum_3 = get_recurring_transaction_sum_on_date(
                self.test_account_1, date_3)
        except:
            raises = True


        self.assertFalse(raises)
        self.assertEqual(self.test_account_1.recurring_transactions.count(), 3)
        self.assertEqual(expected_sum_1, sum_1)
        self.assertEqual(expected_sum_2, sum_2)
        self.assertEqual(expected_sum_3, sum_3)
