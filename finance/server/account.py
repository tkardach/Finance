import json
from flask import request, jsonify, Response, Blueprint, current_app
from flask_login import current_user, login_required
from finance.shared import HTTPErrorResponse, Validation, HTTPResponse
from finance.utility.security import check_hashed_string
from finance.database.models import Account, RecurringTransaction, SingleTransaction


account = Blueprint('account', __name__)


def recurring_transaction_to_dict(transaction: RecurringTransaction) -> dict:
    return {
        'transaction_id': transaction.transaction_id,
        'name': transaction.name,
        'start_date': transaction.start_date,
        'timespan': transaction.timespan,
        'amount': round(float(transaction.amount), 2)
    }


def single_transaction_to_dict(transaction: SingleTransaction) -> dict:
    return {
        'transaction_id': transaction.transaction_id,
        'name': transaction.name,
        'date': transaction.date,
        'amount': round(float(transaction.amount), 2)
    }


def account_to_dict(account: Account) -> dict:
    return {
        'account_id': account.account_id,
        'name': account.name,
        'balance': round(float(account.balance), 2),
        'recurring_transactions': [recurring_transaction_to_dict(i) for i in account.recurring_transactions],
        'single_transactions': [single_transaction_to_dict(i) for i in account.single_transactions]
    }


@account.route('/accounts', methods=['GET'])
@login_required
def get_accounts():
    dict_accounts = [account_to_dict(i) for i in current_user.accounts]

    return HTTPResponse.return_json_response(dict_accounts, 200)