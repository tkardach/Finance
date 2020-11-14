import mysql.connector
from finance.mysql import get_connection
from enum import Enum


class Account:
  ID = 0
  NAME = 1
  PROFILE_ID = 2
  BALANCE = 3


def create_account(profile_id: int, name: str, balance: float = 0) -> None:
  """Creates an account in the database

  Parameters
  ----------
  profile_id: int
    ID of the profile the account will be made for

  name: str
    Name of the account

  balance: float
    Monitary balance of the account

  Raises
  ------
  mysql.connector.Error
    If the connection was unsuccessful; if the query was unsuccessful
  """
  cnx = get_connection()

  cursor = cnx.cursor()
  sql = 'INSERT INTO account (balance, name, profile) VALUES (%s, %s, %s)'
  cursor.execute(sql, (balance, name, profile_id))
  cnx.commit()

  cursor.close()
  cnx.close()


def get_accounts() -> list:
  """Gets all accounts stored in the database

  Returns
  -------
  list
    List of all accounts in the database

  Raises
  ------
  mysql.connector.Error
    If the connection was unsuccessful; if the query was unsuccessful
  """
  cnx = get_connection()

  cursor = cnx.cursor()
  cursor.execute("SELECT * FROM account")
  result = cursor.fetchall()

  cursor.close()
  cnx.close()

  return result


def get_accounts_for_profile(profile_id: int) -> list:
  """Gets all accounts stored in the database for a specific profile

  Parameters
  ----------
  profile_id: int
    The ID of the profile whose accounts will be returned

  Returns
  -------
  list
    List of all accounts belonging to the specified profile

  Raises
  ------
  mysql.connector.Error
    If the connection was unsuccessful; if the query was unsuccessful
  """
  cnx = get_connection()

  cursor = cnx.cursor()
  sql = "SELECT * FROM account WHERE profile=%d" % profile_id
  cursor.execute(sql)
  result = cursor.fetchall()

  cursor.close()
  cnx.close()

  return result


def get_account_by_name_and_profile(name: str, profile_id: int) -> tuple:
  """Gets the account with the specified name belonging to the specified profile

  Parameters
  ----------
  profile: int
    ID of the profile being which owns the account

  name: str
    Name of the account

  Returns
  -------
  tuple
    The account with the matching ID
    
  None
    If the account with ID could not be found

  Raises
  ------
  mysql.connector.Error
    If the connection was unsuccessful; if the query was unsuccessful
  """
  cnx = get_connection()

  cursor = cnx.cursor()
  sql = "SELECT * FROM account WHERE profile=%d AND name='%s'" % (profile_id, name)
  cursor.execute(sql)
  result = cursor.fetchone()

  cursor.close()
  cnx.close()

  return result


def get_account_by_id(id: int) -> tuple:
  cnx = get_connection()

  cursor = cnx.cursor()
  sql = """
  SELECT * 
  FROM account 
  WHERE account_id=%d
  """ % (id)
  cursor.execute(sql)
  result = cursor.fetchone()

  cursor.close()
  cnx.close()

  return result


def get_account_id(name: str, profile_id: int) -> int:
  cnx = get_connection()

  cursor = cnx.cursor()
  sql = """
  SELECT account_id 
  FROM account 
  WHERE profile=%d 
  AND name='%s'
  """ % (profile_id, name)
  cursor.execute(sql)
  result = cursor.fetchone()

  cursor.close()
  cnx.close()

  return result[0]


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

