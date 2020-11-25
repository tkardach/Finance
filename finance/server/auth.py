from finance.database.user import get_user_by_email, create_user
from finance.database.database import SessionLocal
from flask import request, jsonify, Response, Blueprint, current_app
from flask_login import login_user, login_required, logout_user
from flask_security.recoverable import send_reset_password_instructions
from finance.shared import HTTPErrorResponse, Validation
from finance.utility.security import check_hashed_string


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['POST'])
def login():
    # get the request parameters
    email = None
    password = None
    if request.is_json:
        request_json = request.get_json()
        email = request_json.get('email')
        password = request_json.get('password')
    else:
        email = request.form['email']
        password = request.form['password']

    # make sure all parameters exist
    if email is None:
        return HTTPErrorResponse.raise_missing_parameter('email')
    
    if password is None:
        return HTTPErrorResponse.raise_missing_parameter('password')

    # make sure email is a valid email address
    if not Validation.validate_email(email):
        return HTTPErrorResponse.raise_invalid_email(email)

    # check for user in the database
    user = get_user_by_email(current_app.session, email)

    if not user or not check_hashed_string(password, user.password):
        return HTTPErrorResponse.raise_invalid_credentials()

    # login the user
    login_user(user, remember=True)

    return Response(status=200)


@auth.route('/signup', methods=['POST'])
def signup():
    # get the request parameters
    email = None
    password = None
    if request.is_json:
        request_json = request.get_json()
        email = request_json.get('email')
        password = request_json.get('password')
    else:
        email = request.form['email']
        password = request.form['password']

    # make sure all parameters exist
    if email is None:
        return HTTPErrorResponse.raise_missing_parameter('email')
    
    if password is None:
        return HTTPErrorResponse.raise_missing_parameter('password')

    if not Validation.validate_email(email):
        return HTTPErrorResponse.raise_invalid_email(email)

    # make sure email is a valid email address
    user = get_user_by_email(current_app.session, email)

    # check for user is already in the database
    if user:
        return HTTPErrorResponse.raise_user_already_exists()

    # create the user
    new_user = create_user(current_app.session, email, password)

    return Response(status=200)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return Response(status=200)
