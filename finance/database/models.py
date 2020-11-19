from .database import Base
import finance.utility.security as sec
from sqlalchemy import Column, INT, VARCHAR, BOOLEAN, DECIMAL, ForeignKey, DATETIME, Index
from sqlalchemy.orm import relationship
import uuid


def generate_uuid():
   return str(uuid.uuid4())


class User(Base):
    __tablename__ = 'users'

    def __init__(self, email, password, is_admin):
        self.email = email
        self.password = sec.get_hashed_string(password)
        self.is_admin = is_admin


    user_id = Column(
        VARCHAR(36),
        primary_key=True,
        nullable=False,
        index=True,
        default=generate_uuid)
    email = Column(
        VARCHAR(255),
        nullable=False,
        unique=True,
        index=True)
    is_admin = Column(
        BOOLEAN,
        nullable=False)
    password = Column(VARCHAR(255))

    accounts = relationship("Account", back_populates="user")

    def __repr__(self):
        return "<User(email='%s', is_admin='%s')>" % (self.email, self.is_admin)


class Account(Base):
    __tablename__ = 'accounts'

    account_id = Column(
        VARCHAR(36),
        nullable=False,
        unique=True,
        primary_key=True,
        index=True,
        default=generate_uuid)
    name = Column(
        VARCHAR(45),
        primary_key=True)
    user_id = Column(
        VARCHAR(36),
        ForeignKey('users.user_id'),
        primary_key=True)
    balance = Column(
        DECIMAL(15, 2),
        nullable=False
    )

    user = relationship("User", back_populates="accounts")
    recurring_transactions = relationship("RecurringTransaction", back_populates="account")
    single_transactions = relationship("SingleTransaction", back_populates="account")

    __table_args__ = (Index('account_index', 'name', 'user_id'),)

    def __repr__(self):
        return "<Account(name='%s', balance='%.2f')>" % (self.name, self.balance)


class RecurringTransaction(Base):
    __tablename__ = 'recurring_transactions'

    transaction_id = Column(
        'recurring_transaction_id',
        VARCHAR(36),
        primary_key=True,
        nullable=False,
        index=True,
        default=generate_uuid)
    name = Column(
        VARCHAR(45),
        nullable=False
    )
    account_id = Column(
        VARCHAR(36),
        ForeignKey('accounts.account_id'),
        nullable=False)
    start_date = Column(
        DATETIME,
        nullable=False)
    timespan = Column(
        VARCHAR(45),
        nullable=False
    )
    amount = Column(
        DECIMAL(15, 2),
        nullable=False
    )

    account = relationship("Account", back_populates="recurring_transactions")


class SingleTransaction(Base):
    __tablename__ = 'single_transactions'

    transaction_id = Column(
        'single_transaction_id',
        VARCHAR(36),
        primary_key=True,
        nullable=False,
        index=True,
        default=generate_uuid)
    name = Column(
        VARCHAR(45),
        nullable=False
    )
    account_id = Column(
        VARCHAR(36),
        ForeignKey('accounts.account_id'),
        nullable=False)
    date = Column(
        DATETIME,
        nullable=False)
    amount = Column(
        DECIMAL(15, 2),
        nullable=False
    )

    account = relationship("Account", back_populates="single_transactions")