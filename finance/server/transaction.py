from finance.database.user import get_user_by_email, create_user
from finance.database.database import SessionLocal
from flask import request, jsonify, Response, Blueprint, current_app
from flask_login import current_user, login_required
from finance.shared import HTTPErrorResponse, Validation


transaction = Blueprint('transaction', __name__)


def create_single_transaction():
    # expecting json request body
    if not request.is_json:
        return HTTPErrorResponse.post_expects_json()

    request_json = request.get_json()
    account_id = request_json.get('account_id')
    name = request_json.get('name')
    amount = request_json.get('amount')
    date = request_json.get('date')

    return HTTPErrorResponse.invalid_email('buba')

@transaction.route('/single-transaction', methods=['POST', 'GET'])
@login_required
def single_transactions():
    if request.method == 'POST':
        return create_single_transaction()
    elif request.method == 'GET':
        pass