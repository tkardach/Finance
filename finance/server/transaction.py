import finance.database.transactions as transactions
from finance.database.user import get_user_by_email
from finance.database.account import get_user_account_by_id
from finance.database.database import SessionLocal
from flask import request, jsonify, Response, Blueprint, current_app
from flask_login import current_user, login_required
from finance.shared import HTTPErrorResponse, Validation, HTTPResponse, Timespan
from finance.server.shared import single_transaction_to_dict, recurring_transaction_to_dict
from dateutil import parser


transaction = Blueprint('transaction', __name__)


#region Single Transactions

def create_single_transaction():
    # get the request parameters
    account_id = None
    name = None
    amount = None
    post_date = None
    if request.is_json:
        request_json = request.get_json()
        account_id = request_json.get('account_id')
        name = request_json.get('name')
        amount = request_json.get('amount')
        post_date = request_json.get('date')
    else:
        account_id = request.form['account_id']
        name = request.form['name']
        amount = request.form['amount']
        post_date = request.form['date']

    # get date from string
    date = None
    try:
        date = parser.parse(post_date)
    except Exception as err:
        if err is ValueError:
            return HTTPErrorResponse.raise_invalid_parameter('date', "Invalid date format '%s'" % post_date)
        if err is OverflowError:
            return HTTPErrorResponse.raise_invalid_parameter('date', "Date parameter caused OverflowError")

    # get user account with ID for current user
    user_account = get_user_account_by_id(account_id, current_user)

    if user_account is None:
        return HTTPErrorResponse.raise_not_found('User Account with account_id')

    # create transaction
    new_transaction = transactions.create_single_transaction(
        account=user_account, name=name, date=date, amount=amount
    )

    if new_transaction is None:
        HTTPErrorResponse.raise_internal_server_error('Failed to create new single transaction')

    return HTTPResponse.return_json_response(single_transaction_to_dict(new_transaction), 200)


@transaction.route('/single-transactions', methods=['POST'])
@login_required
def create_single_transactions():
    return create_single_transaction()


@transaction.route('/single-transactions/<uuid:account_id>', methods=['GET'])
@login_required
def get_single_transactions(account_id):
    # get user account with ID for current user
    account = get_user_account_by_id(account_id=str(account_id), user=current_user)

    if account is None:
        return HTTPErrorResponse.raise_not_found('Account with id')

    # create list of all single transactions in account as dict
    dict_accounts = [single_transaction_to_dict(i) for i in account.single_transactions]

    return HTTPResponse.return_json_response(dict_accounts, 200)


#endregion

#region Recurring Transactions


def create_recurring_transaction():
    # get the request parameters
    account_id = None
    name = None
    amount = None
    post_date = None
    timespan_str = None
    if request.is_json:
        request_json = request.get_json()
        account_id = request_json.get('account_id')
        name = request_json.get('name')
        amount = request_json.get('amount')
        timespan_str = request_json.get('timespan')
        post_date = request_json.get('start_date')
    else:
        account_id = request.form['account_id']
        name = request.form['name']
        amount = request.form['amount']
        timespan_str = request.form['timespan']
        post_date = request.form['start_date']

    # get date from string
    date = None
    try:
        date = parser.parse(post_date)
    except Exception as err:
        if err is ValueError:
            return HTTPErrorResponse.raise_invalid_parameter('start_date', "Invalid date format '%s'" % post_date)
        if err is OverflowError:
            return HTTPErrorResponse.raise_invalid_parameter('start_date', "Date parameter caused OverflowError")

    # check timespan
    timespan = Timespan.get_timespan(timespan_str)
    if timespan is None:
        return HTTPErrorResponse.raise_invalid_parameter('timespan', "'%s' is an invalid timespan format." % timespan)

    # get user account with ID for current user
    user_account = get_user_account_by_id(account_id, current_user)

    if user_account is None:
        return HTTPErrorResponse.raise_not_found('User Account with account_id')

    # create transaction
    new_transaction = transactions.create_recurring_transaction(
        account=user_account, name=name, start_date=date, amount=amount, timespan=timespan
    )

    if new_transaction is None:
        HTTPErrorResponse.raise_internal_server_error(
            'Failed to create new recurring transaction')

    return HTTPResponse.return_json_response(recurring_transaction_to_dict(new_transaction), 200)


@transaction.route('/recurring-transactions', methods=['POST'])
@login_required
def create_recurring_transactions():
    return create_recurring_transaction()


@transaction.route('/recurring-transactions/<uuid:account_id>', methods=['GET'])
@login_required
def get_recurring_transactions(account_id):
    # get user account with ID for current user
    account = get_user_account_by_id(account_id=str(account_id), user=current_user)

    if account is None:
        return HTTPErrorResponse.raise_not_found('Account with id')

    # create list of all recurring transactions in account as dict
    dict_accounts = [recurring_transaction_to_dict(i) for i in account.recurring_transactions]

    return HTTPResponse.return_json_response(dict_accounts, 200)


#endregion