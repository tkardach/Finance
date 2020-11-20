from typing import List
from .models import User
from .database import SessionLocal


def create_user(
        session: SessionLocal,
        email: str,
        password: str,
        is_admin: bool = False) -> User:
    """Creates a user in the database

    Parameters
    ----------
    email : str
      email for the new user
    password : str
      password for the new user

    Raises
    ------
    SQLAlchemyError
      When creating user was unsuccessful
      When session add was unsuccessful
    """
    user = User(
        email=email,
        password=password,
        is_admin=is_admin
    )
    session.add(user)

    return user


def get_users(session: SessionLocal) -> List[User]:
    """Get all users listed in the database

    Returns
    -------
    List[User]
      A list of all users in the database

    Raises
    ------
    SQLAlchemyError
      When session query was unsuccessul
    """
    return session.query(User).all()


def get_user_by_email(session: SessionLocal, email: str) -> User:
    """Get the user id given the user email

    Parameters
    ----------
    session: SessionLocal
      The current database session

    email: str
      The email of the desired user

    Returns
    -------
    User
      The user with the given email

    None
      If no user was found

    Raises
    ------
    SQLAlchemyError
      When session query was unsuccessul
    """
    return session.query(User).filter(User.email == email).scalar()


def get_user_by_id(session: SessionLocal, user_id: str) -> User:
    """Get the user given the user ID

    Parameters
    ----------
    session: SessionLocal
      The current database session

    user_id: str
      The id of the desired User

    Returns
    -------
    User
      User with the given ID

    None
      If no user was found

    Raises
    ------
    SQLAlchemyError
      When session query was unsuccessul
    """
    return session.query(User).filter(User.user_id == user_id).scalar()
