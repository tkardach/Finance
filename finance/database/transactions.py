from typing import List
from finance.shared import Timespan
from .models import Account, SingleTransaction, RecurringTransaction
from .database import SessionLocal
from sqlalchemy import func
from datetime import date, datetime, timedelta
from dateutil.relativedelta import relativedelta


# region SingleTransaction


def create_single_transaction(
        account: Account,
        name: str,
        date: date,
        amount: float = 0.0) -> SingleTransaction:
    """Creates an single transaction in the database for the 
    specified account

    Parameters
    ----------
    account : Account
      Account the transaction is for
    name : str
      Name of the transaction
    date : date
      Date of the transaction
    amount : float
      Amount of the transaction

    Returns
    -------
    SingleTransaction
      The SingleTransaction which was just created
    """
    if account is None:
        return None

    trans = SingleTransaction(
        name=name, account_id=account.account_id, date=date, amount=amount)
    account.single_transactions.append(trans)
    return trans


def get_all_single_transactions_on_date(
        account: Account,
        date: date) -> List[SingleTransaction]:
    """Gets all single transactions for an account up to the
    specified date

    Parameters
    ----------
    account : Account
      Account the transaction is for
    date : date
      Latest date for transactions

    Returns
    -------
    List[SingleTransaction]
      List of all transactions up to the given date
    """
    return account.single_transactions.filter(
        SingleTransaction.date <= date
    ).all()


def get_single_transaction_sum_on_date(
        account: Account,
        date: date) -> float:
    """Gets the sum of all single transactions for an account
    up to the specified date

    Parameters
    ----------
    account : Account
      Account the transaction is for
    date : date
      Latest date for transactions

    Returns
    -------
    float
      The total of all single transactions up to the date
    """
    result = account.single_transactions.with_entities(
        func.sum(SingleTransaction.amount).label('total_sum')
    ).filter(
        SingleTransaction.date <= date
    ).scalar()
    if result is None:
        return 0
    return round(float(result), 2)


# endregion


# region RecurringTransaction
 

def create_recurring_transaction(
        account: Account,
        name: str,
        start_date: date,
        timespan: Timespan,
        amount: float = 0.0)->RecurringTransaction:
    """Creates a recurring transaction in the database for the 
    specified account

    Parameters
    ----------
    account : Account
      Account the transaction is for
    name : str
      Name of the transaction
    start_date : date
      Starting date of the transaction
    timespan : Timespan
      Frequency of the transaction
    amount : float
      Amount of the transaction

    Returns
    -------
    RecurringTransaction
      The RecurringTransaction which was just created
    """
    if account is None:
        return None
    trans = RecurringTransaction(
        account_id=account.account_id,
        name=name, 
        start_date=start_date, 
        timespan=timespan.to_timespan_str(), 
        amount=amount
      )
    account.recurring_transactions.append(trans)
    return trans


def get_all_recurring_transactions_on_date(
        account: Account,
        date: date) -> List[RecurringTransaction]:
    """Gets all recurring transactions for an account up to the
    specified date

    Parameters
    ----------
    account : Account
      Account the transaction is for
    date : date
      Latest date for transactions

    Returns
    -------
    List[RecurringTransaction]
      List of all transactions up to the given date
    """
    return account.recurring_transactions.filter(
        RecurringTransaction.start_date <= date
    ).all()


def get_recurring_transaction_sum_on_date(
        account: Account,
        date: date) -> float:
    """Gets the sum of all recurring transactions for an account
    up to the specified date

    Parameters
    ----------
    account : Account
      Account the transaction is for
    date : date
      Latest date for transactions

    Returns
    -------
    float
      The total of all recurring transactions up to the date
    """
    transactions = get_all_recurring_transactions_on_date(account, date)
    
    transaction_sum = 0
    for transaction in transactions:
        timespan = Timespan.get_timespan(transaction.timespan)
        start_date = transaction.start_date.date()
        amount = float(transaction.amount)

        # continue itterating through timespans to see how many 
        # recurring transactions occurred
        num_of_timespans = 1
        while start_date < date:
            start_date = start_date + relativedelta(
              years=+timespan.years,
              months=+timespan.months,
              weeks=+timespan.weeks,
              days=+timespan.days)
            if start_date <= date:
                num_of_timespans = num_of_timespans + 1

        transaction_sum = transaction_sum + (num_of_timespans * amount)

    return round(transaction_sum, 2)


# endregion


# region Account Calculations


def get_account_balance_on_date(
        account: Account,
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
    balance = float(account.balance)
    single_amount = get_single_transaction_sum_on_date(
        account,
        date
    )

    recurring_amount = get_recurring_transaction_sum_on_date(
        account,
        date
    )

    return round(balance + single_amount + recurring_amount, 2)


# endregion