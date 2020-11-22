from finance.database.models import RecurringTransaction, SingleTransaction, Account


def recurring_transaction_to_dict(transaction: RecurringTransaction) -> dict:
    """Convert a RecurringTransaction object into a dict

    Parameters
    ----------
    transaction: RecurringTransaction
        The RecurringTransaction to transform into a dict

    Returns
    -------
    dict
        dict containing fields from RecurringTransaction
    """
    if transaction is None:
        return None
    return {
        'transaction_id': transaction.transaction_id,
        'name': transaction.name,
        'start_date': transaction.start_date.strftime('%m-%d-%Y'),
        'timespan': transaction.timespan,
        'amount': round(float(transaction.amount), 2)
    }


def single_transaction_to_dict(transaction: SingleTransaction) -> dict:
    """Convert a SingleTransaction object into a dict

    Parameters
    ----------
    transaction: SingleTransaction
        The SingleTransaction to transform into a dict

    Returns
    -------
    dict
        dict containing fields from SingleTransaction
    """
    if transaction is None:
        return None
    return {
        'transaction_id': transaction.transaction_id,
        'name': transaction.name,
        'date': transaction.date.strftime('%m-%d-%Y'),
        'amount': round(float(transaction.amount), 2)
    }


def account_to_dict(account: Account) -> dict:
    """Convert a Account object into a dict

    Parameters
    ----------
    account: Account
        The Account to transform into a dict

    Returns
    -------
    dict
        dict containing fields from Account
    """
    if account is None:
        return None
    return {
        'account_id': account.account_id,
        'name': account.name,
        'balance': round(float(account.balance), 2),
        'recurring_transactions': [recurring_transaction_to_dict(i) for i in account.recurring_transactions],
        'single_transactions': [single_transaction_to_dict(i) for i in account.single_transactions]
    }

