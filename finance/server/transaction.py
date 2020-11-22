import finance.database.transactions as transactions
from finance.database.user import get_user_by_email
from finance.database.account import get_user_account_by_id
from finance.database.database import SessionLocal
from flask import request, jsonify, Response, Blueprint, current_app
from flask_login import current_user, login_required
from finance.shared import HTTPErrorResponse, Validation, HTTPResponse
from finance.server.shared import single_transaction_to_dict
from dateutil import parser


transaction = Blueprint('transaction', __name__)


def create_single_transaction():
    # expecting json request body
    if not request.is_json:
        return HTTPErrorResponse.post_expects_json()

    request_json = request.get_json()
    account_id = request_json.get('account_id')
    name = request_json.get('name')
    amount = request_json.get('amount')
    post_date = request_json.get('date')

    date = None
    try:
        date = parser.parse(post_date)
    except Exception as err:
        if err is ValueError:
            return HTTPErrorResponse.invalid_parameter('date', "Invalid date format '%s'" % post_date)
        if err is OverflowError:
            return HTTPErrorResponse.invalid_parameter('date', "Date parameter caused OverflowError")

    user_account = get_user_account_by_id(account_id, current_user)

    if user_account is None:
        return HTTPErrorResponse.not_found('User Account with account_id')

    new_transaction = transactions.create_single_transaction(
        account=user_account, name=name, date=date, amount=amount
    )

    if new_transaction is None:
        HTTPErrorResponse.internal_server_error(
            'Failed to create new single transaction')

    return HTTPResponse.return_json_response(single_transaction_to_dict(new_transaction), 200)


@transaction.route('/single-transaction', methods=['POST', 'GET'])
@login_required
def single_transactions():
    if request.method == 'POST':
        return create_single_transaction()
    elif request.method == 'GET':
        # TODO should have GET method be by account id, so we return only accounts transactions
        dict_accounts = [single_transaction_to_dict(
            i) for i in current_user.accounts]

        return HTTPResponse.return_json_response(dict_accounts, 200)
