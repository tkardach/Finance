from finance.utility.config import Config
from finance.database.database import SessionLocal
from sqlalchemy.orm import scoped_session
from flask import Flask, _app_ctx_stack


app = Flask(__name__)
app.secret_key = Config.secret_key


@app.before_request
def create_session():
  app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)


@app.teardown_appcontext
def shutdown_session(response_or_exc):
  app.session.commit()
  app.session.remove()