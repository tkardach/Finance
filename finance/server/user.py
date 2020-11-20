import json
from flask import request, jsonify, Response, Blueprint, current_app
from flask_login import current_user, login_required
from finance.shared import HTTPErrorResponse, Validation, HTTPResponse
from finance.utility.security import check_hashed_string


user = Blueprint('user', __name__)


@user.route('/profile', methods=['GET'])
@login_required
def profile():
    user = {
        'email': current_user.email
    }
    return HTTPResponse.return_json_response(user, 200)
