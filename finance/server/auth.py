from finance.database.user import get_user_by_email, create_user
from finance.database.database import SessionLocal
from finance.server import app
from flask import request, jsonify, Response, Blueprint, current_app
from flask_login import login_user, login_required, logout_user
from finance.shared import HTTPErrorResponse, Validation
from finance.utility.security import check_hashed_string


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    # expecting json request body
    if not request.is_json:
        return HTTPErrorResponse.post_expects_json()
    
    request_json = request.get_json()
    email = request_json.get('email')
    password = request_json.get('password')

    # make sure all parameters exist
    if email is None:
        return HTTPErrorResponse.post_missing_parameters('email')
    
    if password is None:
        return HTTPErrorResponse.post_missing_parameters('password')

    # make sure email is a valid email address
    if not Validation.validate_email(email):
        return HTTPErrorResponse.invalid_email(email)

    # check for user in the database
    user = get_user_by_email(current_app.session, email)

    if not user or not check_hashed_string(password, user.password):
        return HTTPErrorResponse.post_invalid_credentials()

    # login the user
    login_user(user, remember=True)

    return Response(status=200)


@auth.route('/signup', methods=['POST'])
def signup():
    # expecting json request body
    if not request.is_json:
        return HTTPErrorResponse.post_expects_json()
    
    request_json = request.get_json()
    email = request_json.get('email')
    password = request_json.get('password')

    # make sure all parameters exist
    if email is None:
        return HTTPErrorResponse.post_missing_parameters('email')
    
    if password is None:
        return HTTPErrorResponse.post_missing_parameters('password')

    if not Validation.validate_email(email):
        return HTTPErrorResponse.invalid_email(email)

    # make sure email is a valid email address
    user = get_user_by_email(current_app.session, email)

    # check for user is already in the database
    if user:
        return HTTPErrorResponse.user_already_exists()

    # create the user
    new_user = create_user(current_app.session, email, password)

    return Response(status=200)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return Response(status=200)