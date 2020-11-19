from typing import List
from .models import User, Account
from .database import SessionLocal


def create_account(name: str, user: User, balance: float = 0) -> Account:
    """Creates an account in the database

    Parameters
    ----------
    name : str
      Name of the account
    balance : float
      Balance of the account
    user : User
      User the account belongs to

    Returns
    -------
    Account
      The account which was created

    Raises
    ------
    SQLAlchemyError
      When creating account was unsuccessful
      When session add was unsuccessful
    """
    if user is None:
        return None
    
    account = Account(
        name=name,
        balance=balance
    )
    user.accounts.append(account)
    return account


def get_accounts(session: SessionLocal) -> List[Account]:
    """Gets all accounts stored in the database

    Returns
    -------
    List[Account]
      List of all accounts in the database

    Raises
    ------
    SQLAlchemyError
      When session add was unsuccessful
    """
    return session.query(Account).all()


def get_account_balance(account_id: int) -> float:
    cnx = get_connection()

    cursor = cnx.cursor()
    sql = """
    SELECT balance 
    FROM account 
    WHERE account_id=%d
    """ % (account_id)
    cursor.execute(sql)
    result = cursor.fetchone()

    cursor.close()
    cnx.close()

    return float(result[0])
