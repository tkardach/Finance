import json
from flask import request, jsonify, Response, Blueprint, current_app
from flask_login import current_user, login_required
from finance.shared import HTTPErrorResponse, Validation, HTTPResponse
from finance.utility.security import check_hashed_string
from finance.database.models import Account, RecurringTransaction, SingleTransaction
from finance.database.user import get_user_by_email
from finance.server.shared import *
import finance.database.account as acc


account = Blueprint('account', __name__)


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
