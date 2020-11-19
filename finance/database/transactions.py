from typing import List
from finance.shared import *
from .models import Account, SingleTransaction, RecurringTransaction
from .database import SessionLocal
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


#region SingleTransaction


def create_single_transaction(
        account: Account,
        name: str,
        datetime: datetime,
        amount: float = 0.0) -> SingleTransaction:
    """Creates an single transaction in the database for the 
    specified account

    Parameters
    ----------
    account : Account
      Account the transaction is for
    name : str
      Name of the transaction
    datetime : datetime
      Date of the transaction
    amount : float
      Amount of the transaction

    Returns
    -------
    SingleTransaction
      The SingleTransaction which was just created

    Raises
    ------
    SQLAlchemyError
      When creating SingleTransaction was unsuccessful
      When session add was unsuccessful
    """
    if account is None:
        return None

    trans = SingleTransaction(
        name=name, account_id=account.account_id, date=date, amount=amount)
    account.single_transactions.append(trans)
    return trans


#endregion

def create_recurring_transaction(
        account_id: int,
        trans_name: str,
        start_date: date,
        timespan: Timespan,
        amount: float = 0.0):
    cnx = get_connection()

    cursor = cnx.cursor()
    sql = """
  INSERT INTO recurring_transaction (account, name, start_date, amount, timespan) 
  VALUES (%s, %s, %s, %s, %s)
  """
    cursor.execute(sql, (account_id, trans_name, start_date,
                         amount, timespan.to_timespan_str()))
    cnx.commit()

    cursor.close()
    cnx.close()


def get_all_single_transactions_for_account(account_id: int) -> list:
    """Get all single transactions for the specified account

    Returns
    -------
    list
      A list of all single transactions for account in the database

    Raises
    ------
    mysql.connector.Error
      If the connection was unsuccessful; if the query was unsuccessful
    """
    cnx = get_connection()

    cursor = cnx.cursor()
    sql = """
  SELECT * FROM single_transaction 
  WHERE account=%d
  """ % (account_id)
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    cnx.close()

    return result


def get_all_recurring_transactions_for_account(account_id: int) -> list:
    """Get all recurring transactions for the specified account

    Returns
    -------
    list
      A list of all recurring transactions for account in the database

    Raises
    ------
    mysql.connector.Error
      If the connection was unsuccessful; if the query was unsuccessful
    """
    cnx = get_connection()

    cursor = cnx.cursor()
    sql = """
  SELECT * FROM recurring_transaction 
  WHERE account=%d
  """ % (account_id)
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    cnx.close()

    return result


def get_all_single_transactions_for_account_from_date(
        account_id: int,
        date: date) -> list:
    """Get all single transactions for the specified account

    Returns
    -------
    list
      A list of all single transactions for account in the database

    Raises
    ------
    mysql.connector.Error
      If the connection was unsuccessful; if the query was unsuccessful
    """
    cnx = get_connection()

    cursor = cnx.cursor()
    sql = """
  SELECT * FROM single_transaction 
  WHERE account=%d
  AND DATE(date)<='%s'
  """ % (account_id, date_to_mysql_str(date))
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    cnx.close()

    return result


def get_all_recurring_transactions_for_account_from_date(
        account_id: int,
        date: date) -> list:
    """Get all recurring transactions for the specified account

    Returns
    -------
    list
      A list of all recurring transactions for account in the database

    Raises
    ------
    mysql.connector.Error
      If the connection was unsuccessful; if the query was unsuccessful
    """
    cnx = get_connection()

    cursor = cnx.cursor()
    sql = """
  SELECT * FROM recurring_transaction 
  WHERE account=%d
  AND DATE(start_date)<='%s'
  """ % (account_id, date_to_mysql_str(date))
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    cnx.close()

    return result


def get_single_transaction_sum_from_date(
        account_id: int,
        date: date) -> float:
    """Get the sum of all single transactions before the given date

    Parameters
    ----------
    account_id: int
      ID of the account

    date: date
      Date to use as a reference

    Returns
    -------
    float
      Sum of all single transactions before the given date for the account

    Raises
    ------
    mysql.connector.Error
      If the connection was unsuccessful; if the query was unsuccessful
    """
    cnx = get_connection()

    cursor = cnx.cursor()
    sql = """
  SELECT SUM(amount) FROM single_transaction 
  WHERE account=%d
  AND DATE(date)<='%s'
  """ % (account_id, date_to_mysql_str(date))
    cursor.execute(sql)
    result = cursor.fetchone()

    cursor.close()
    cnx.close()

    return float(result[0])


def get_recurring_transaction_sum_from_date(
        account_id: int,
        date: date) -> float:
    """Get the sum of all recurring transactions before the given date

    Parameters
    ----------
    account_id: int
      ID of the account

    date: date
      Date to use as a reference

    Returns
    -------
    float
      Sum of all recurring transactions before the given date for the account

    Raises
    ------
    mysql.connector.Error
      If the connection was unsuccessful; if the query was unsuccessful
    """
    cnx = get_connection()

    cursor = cnx.cursor()
    sql = """
  SELECT * FROM recurring_transaction 
  WHERE account=%d
  AND DATE(start_date)<='%s'
  """ % (account_id, date_to_mysql_str(date))
    cursor.execute(sql)
    result = cursor.fetchall()

    cursor.close()
    cnx.close()

    transaction_sum = 0
    for transaction in result:
        timespan = Timespan.get_timespan(
            transaction[RecurringTransaction.TIMESPAN])
        start_date = transaction[RecurringTransaction.START_DATE].date()
        amount = float(transaction[RecurringTransaction.AMOUNT])

        num_of_timespans = 0
        while start_date < date:
            start_date = start_date + relativedelta(years=+timespan.years)
            start_date = start_date + relativedelta(months=+timespan.months)
            start_date = start_date + relativedelta(weeks=+timespan.weeks)
            start_date = start_date + relativedelta(days=+timespan.days)

            if start_date <= date:
                num_of_timespans = num_of_timespans + 1

        transaction_sum = transaction_sum + (num_of_timespans * amount)

    return transaction_sum


def get_account_balance_for_date(
        profile_id: int,
        account_name: str,
        date: date) -> float:
    """Get the account balance on a given date

    Parameters
    ----------
    profile_id: int
      ID of the profile being checked

    account_name: str
      Name of the account being checked

    Returns
    -------
    float
      Sum of all transactions and initial account balance on the given date

    Raises
    ------
    mysql.connector.Error
      If the connection was unsuccessful; if the query was unsuccessful
    """
    account_id = get_account_id(
        name=account_name,
        profile_id=profile_id)

    return get_account_balance_for_date_by_id(
        account_id,
        date)


def get_account_balance_for_date_by_id(
        account_id: int,
        date: date) -> float:
    """Get the account balance on a given date

    Parameters
    ----------
    account_id: int
      ID of the account

    Returns
    -------
    float
      Sum of all transactions and initial account balance on the given date

    Raises
    ------
    mysql.connector.Error
      If the connection was unsuccessful; if the query was unsuccessful
    """
    balance = get_account_balance(account_id)
    single_amount = get_single_transaction_sum_from_date(
        account_id,
        date
    )

    recurring_amount = get_recurring_transaction_sum_from_date(
        account_id,
        date
    )

    return balance + single_amount + recurring_amount
