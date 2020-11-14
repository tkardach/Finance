import mysql.connector
from finance.config import Config


def get_connection():
  """Get mysql.connector connection to the database

  Returns
  -------
  mysql.connector connection to the database

  Raises
  ------
  mysql.connector.Error
    If the connection to the database could not be made
  """
  return mysql.connector.connect(
    host=Config.db_host,
    user=Config.db_user,
    password=Config.db_pass,
    database=Config.db_name
  )