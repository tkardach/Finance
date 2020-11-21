from finance.utility.config import Config
from finance.database.database import SessionLocal
from finance.database.models import User
from finance.database.user import get_user_by_id
from sqlalchemy.orm import scoped_session
from flask import Flask, _app_ctx_stack
from flask_login import LoginManager


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


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(app.session, user_id)


@app.before_request
def create_session():
  app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.teardown_appcontext
def shutdown_session(response_or_exc):
  app.session.commit()
  app.session.remove()