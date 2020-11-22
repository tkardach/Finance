from finance.utility.config import Config
from finance.database.database import SessionLocal
from finance.database.models import User
from finance.database.user import get_user_by_id
from sqlalchemy.orm import scoped_session
from flask import Flask, _app_ctx_stack
from flask_login import LoginManager
from finance.shared import HTTPErrorResponse
from finance.utility.logging import logger


app = Flask(__name__)
app.secret_key = Config.secret_key

login_manager = LoginManager(app)

# Initialize routes
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

from .user import user as user_blueprint
app.register_blueprint(user_blueprint)

from .account import account as account_blueprint
app.register_blueprint(account_blueprint)

from .transaction import transaction as transaction_blueprint
app.register_blueprint(transaction_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(app.session, user_id)


# region Flask app session handling


# App before request
# Setup scoped session
@app.before_request
def create_session():
  app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

# App teardown after request
# commit and remove session
@app.teardown_appcontext
def shutdown_session(response_or_exc):
  app.session.commit()
  app.session.remove()

# Error handling
# rollback session
@app.errorhandler(Exception)
def catch_all_errors(error):
  logger.error(error)
  app.session.rollback()
  return HTTPErrorResponse.internal_server_error()
  
# Error handling catch 401 sent from flask login_required
@app.errorhandler(401)
def catch_all_errors(error):
  logger.error(error)
  app.session.rollback()
  return HTTPErrorResponse.unauthorized_user()


# endregion