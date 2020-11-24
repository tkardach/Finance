import json
from flask import request, jsonify, Response, Blueprint, current_app
from flask_login import current_user, login_required
from finance.shared import HTTPErrorResponse, Validation, HTTPResponse
from finance.utility.security import check_hashed_string
from finance.database.models import Account, RecurringTransaction, SingleTransaction
from finance.database.user import get_user_by_email
from finance.database.transactions import get_account_balance_on_date
from finance.server.shared import account_to_dict
from dateutil import parser
import finance.database.account as acc


account = Blueprint('account', __name__)


def create_account():
    """Create an account for the current_user
    """
    session = current_app.session

    name = None
    balance = None
    # get the request parameters
    if request.is_json:
        request_json = request.get_json()
        name = request_json.get('name')
        balance = request_json.get('balance')
    else:
        name = request.form['name']
        balance = request.form['balance']

    email = current_user.email

    # make sure all parameters exist
    if name is None:
        return HTTPErrorResponse.raise_missing_parameter('name')
    
    if balance is None:
        return HTTPErrorResponse.raise_missing_parameter('balance')
    
    if email is None:
        return HTTPErrorResponse.raise_internal_server_error()

    # find user so we can control session (as oppose to using current_user)
    user = get_user_by_email(session=session, email=email)
    user_account = acc.create_account(name=name, balance=balance, user=user)

    return HTTPResponse.return_json_response(account_to_dict(user_account), 200)


@account.route('/accounts', methods=['GET', 'POST'])
@login_required
def get_user_accounts():
    if request.method == 'GET':
        dict_accounts = [account_to_dict(i) for i in current_user.accounts]

        return HTTPResponse.return_json_response(dict_accounts, 200)
    elif request.method == 'POST':
        return create_account()


@account.route('/account/<uuid:account_id>', methods=['GET'])
@login_required
def get_account(account_id):
    # find the user account with the given id
    user_account = current_user.accounts.filter(Account.account_id==str(account_id)).scalar()

    # return 404 if not found
    if user_account is None:
        return HTTPErrorResponse.raise_not_found('Account with id')
    
    # return account as dict
    return HTTPResponse.return_json_response(account_to_dict(user_account), 200)


@account.route('/account/<uuid:account_id>/balance/<date>', methods=['GET'])
@login_required
def get_account_balance(account_id, date):
    # get date from string
    try:
        date = parser.parse(date).date()
    except Exception as err:
        if err is ValueError:
            return HTTPErrorResponse.raise_invalid_parameter('date', "Invalid date format '%s'" % date)
        if err is OverflowError:
            return HTTPErrorResponse.raise_invalid_parameter('date', "Date parameter caused OverflowError")

    # find the user account with the given id
    user_account = current_user.accounts.filter(Account.account_id==str(account_id)).scalar()

    # return 404 if not found
    if user_account is None:
        return HTTPErrorResponse.raise_not_found('Account with id')
    
    # get the account balance on the given date
    balance = get_account_balance_on_date(user_account, date)

    return HTTPResponse.return_json_response({'balance':balance}, 200)