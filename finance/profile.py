import mysql.connector
from finance.mysql import get_connection


def create_profile(email: str, password: str) -> None:
  """Creates a profile in the database

  Parameters
  ----------
  email : str
    email for the new profile
  password : str
    password for the new profile

  Raises
  ------
  mysql.connector.Error
    If the connection was unsuccessful; if the insertion was unsuccessful
  """
  cnx = get_connection()

  cursor = cnx.cursor()
  sql = 'INSERT INTO profile (email, password) VALUES (%s, %s)'
  cursor.execute(sql, (email, password))
  cnx.commit()

  cursor.close()
  cnx.close()


def get_profiles() -> list:
  """Get all profiles listed in the database

  Returns
  -------
  list
    A list of all profiles in the database

  Raises
  ------
  mysql.connector.Error
    If the connection was unsuccessful; if the query was unsuccessful
  """
  cnx = get_connection()

  cursor = cnx.cursor()
  cursor.execute('SELECT profile_id, email FROM profile')
  result = cursor.fetchall()

  cursor.close()
  cnx.close()

  return result


def get_profile_id(email: str) -> int:
  """Get the profile id given the profile email

  Returns
  -------
  int
    The ID of the given profile

  None
    If no profile was found

  Raises
  ------
  mysql.connector.Error
    If the connection was unsuccessful; if the query was unsuccessful
  """
  cnx = get_connection()

  cursor = cnx.cursor()
  sql = "SELECT profile_id FROM profile WHERE email='%s'" % email
  cursor.execute(sql)
  result = cursor.fetchone()

  cursor.close()
  cnx.close()

  return None if not result else result[0]


def get_profile(profile_id: int) -> tuple:
  """Get the profile given the profile id

  Returns
  -------
  tuple
    Profile in the form of a tuple (profile_id, email)

  None
    If the profile was not found

  Raises
  ------
  mysql.connector.Error
    If the connection was unsuccessful; if the query was unsuccessful
  """
  cnx = get_connection()

  cursor = cnx.cursor()
  sql = "SELECT profile_id, email FROM profile WHERE profile_id='{0}'".format(profile_id)
  cursor.execute(sql)
  result = cursor.fetchone()

  cursor.close()
  cnx.close()

  return None if not result else result