from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String

from database import Base


class User(Base):
    """Represents a bank user in the users table."""

    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    name = Column(String)
    # These SQLAlchemy constraints require an email and prevent duplicate values.
    email = Column(String, unique=True, nullable=False)
    # Passing the callable creates a fresh UTC timestamp for each inserted row.
    created_at = Column(DateTime, default=datetime.utcnow)


class Account(Base):
    """Represents a bank account belonging to a user."""

    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True)
    # ForeignKey uses the database table and column name to enforce the account-owner link.
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    # Numeric(10, 2) stores monetary values with fixed precision and two decimal places.
    balance = Column(Numeric(10, 2), default=0)
    account_type = Column(String)
    # The callable is evaluated separately when each account is inserted.
    created_at = Column(DateTime, default=datetime.utcnow)


class Transaction(Base):
    """Represents a financial transaction linked to an account."""

    __tablename__ = "transactions"

    txn_id = Column(Integer, primary_key=True)
    # ForeignKey references the database table so each transaction belongs to an existing account.
    account_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    txn_type = Column(String)
    # Fixed precision represents currency accurately; nullable=False requires an amount.
    amount = Column(Numeric(10, 2), nullable=False)
    # The callable supplies the UTC creation time for each inserted transaction.
    created_at = Column(DateTime, default=datetime.utcnow)
