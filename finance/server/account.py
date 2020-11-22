import json
from flask import request, jsonify, Response, Blueprint, current_app
from flask_login import current_user, login_required
from finance.shared import HTTPErrorResponse, Validation, HTTPResponse
from finance.utility.security import check_hashed_string
from finance.database.models import Account, RecurringTransaction, SingleTransaction
from finance.database.user import get_user_by_email
import finance.database.account as acc


account = Blueprint('account', __name__)


def recurring_transaction_to_dict(transaction: RecurringTransaction) -> dict:
    """Convert a RecurringTransaction object into a dict

    Parameters
    ----------
    transaction: RecurringTransaction
        The RecurringTransaction to transform into a dict

    Returns
    -------
    dict
        dict containing fields from RecurringTransaction
    """
    if transaction is None:
        return None
    return {
        'transaction_id': transaction.transaction_id,
        'name': transaction.name,
        'start_date': transaction.start_date,
        'timespan': transaction.timespan,
        'amount': round(float(transaction.amount), 2)
    }


def single_transaction_to_dict(transaction: SingleTransaction) -> dict:
    """Convert a SingleTransaction object into a dict

    Parameters
    ----------
    transaction: SingleTransaction
        The SingleTransaction to transform into a dict

    Returns
    -------
    dict
        dict containing fields from SingleTransaction
    """
    if transaction is None:
        return None
    return {
        'transaction_id': transaction.transaction_id,
        'name': transaction.name,
        'date': transaction.date,
        'amount': round(float(transaction.amount), 2)
    }


def account_to_dict(account: Account) -> dict:
    """Convert a Account object into a dict

    Parameters
    ----------
    account: Account
        The Account to transform into a dict

    Returns
    -------
    dict
        dict containing fields from Account
    """
    if account is None:
        return None
    return {
        'account_id': account.account_id,
        'name': account.name,
        'balance': round(float(account.balance), 2),
        'recurring_transactions': [recurring_transaction_to_dict(i) for i in account.recurring_transactions],
        'single_transactions': [single_transaction_to_dict(i) for i in account.single_transactions]
    }


def create_account():
    """Create an account for the current_user
    """
    session = current_app.session

    # expecting json request body
    if not request.is_json:
        return HTTPErrorResponse.post_expects_json()
    
    request_json = request.get_json()
    name = request_json.get('name')
    balance = request_json.get('balance')
    email = current_user.email

    # make sure all parameters exist
    if name is None:
        return HTTPErrorResponse.post_missing_parameters('name')
    
    if balance is None:
        return HTTPErrorResponse.post_missing_parameters('balance')
    
    if email is None:
        return HTTPErrorResponse.internal_server_error('Current user email could not be found')

    # find user so we can control session (as oppose to using current_user)
    user = get_user_by_email(session=session, email=email)
    account = acc.create_account(name=name, balance=balance, user=user)

    return HTTPResponse.return_json_response(account_to_dict(account), 200)


@account.route('/accounts', methods=['GET', 'POST'])
@login_required
def accounts():
    if request.method == 'GET':
        dict_accounts = [account_to_dict(i) for i in current_user.accounts]

        return HTTPResponse.return_json_response(dict_accounts, 200)
    elif request.method == 'POST':
        return create_account()
