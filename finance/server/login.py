from finance.server.server import app
import finance.database.profile as profile
from flask import request, jsonify, Response
from flask_login import LoginManager


login_manager = LoginManager(app)


class User():
  def __init__(self, user_id=''):
    self.__user_id = user_id
    self.__is_authenticated = False
    self.__is_active = True
    self.__is_anonymous = True

  @property
  def is_authenticated() -> bool:
    return self.__is_authenticated

  @is_authenticated.setter
  def is_authenticated(self, authenticated):
    self.is_authenticated = authenticated

  @property
  def is_active() -> bool:
    return self.__is_active

  @is_active.setter
  def is_active(self, active):
    self.__is_active = active

  @property 
  def is_anonymous() -> bool:
    return self.__is_anonymous

  @is_anonymous.setter
  def is_anonymous(self, anon):
    self.__is_anonymous = anon

  def get_id(self) -> str:
    return self.__user_id

  @staticmethod
  def get_user(user_id: str) -> 'User':
    try:
      user = profile.get_profile_by_email(user_id)
      if user is not None:
        return User(user[profile.Profile.EMAIL])
      else:
        return None
    except:
      return None


@login_manager.user_loader
def load_user(user_id):
  return profile.get_profile()


@app.route('/login', methods=['POST'])
def login():
  pass