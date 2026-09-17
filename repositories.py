from sqlalchemy.orm import Session

from models import Account, Transaction, User


class UserRepository:
    def create_user(self, db: Session, name: str, email: str):
        """Create and persist a new user record, then return it."""
        user = User(name=name, email=email)
        db.add(user)
        # commit() makes the insert durable in the database; refresh() loads the generated primary key and any defaults back into the object.
        db.commit()
        db.refresh(user)
        return user

    def get_user_by_id(self, db: Session, user_id: int):
        """Return a user by ID or None if no row matches."""
        return db.query(User).filter(User.user_id == user_id).first()

    def get_user_by_email(self, db: Session, email: str):
        """Return a user by email or None if no row matches."""
        return db.query(User).filter(User.email == email).first()


class AccountRepository:
    def create_account(self, db: Session, user_id: int, account_type: str):
        """Create and persist a new account for a user, then return it."""
        account = Account(user_id=user_id, account_type=account_type)
        db.add(account)
        # commit() makes the insert durable in the database; refresh() loads the generated primary key and any defaults back into the object.
        db.commit()
        db.refresh(account)
        return account

    def get_account_by_id(self, db: Session, account_id: int):
        """Return an account by ID or None if no row matches."""
        return db.query(Account).filter(Account.account_id == account_id).first()

    def update_balance(self, db: Session, account: Account, new_balance):
        """Update an existing account's balance and return the refreshed row."""
        account.balance = new_balance
        # Because this object was already attached to the session, SQLAlchemy tracks the change automatically and does not require another add().
        db.commit()
        db.refresh(account)
        return account


class TransactionRepository:
    def create_transaction(self, db: Session, account_id: int, txn_type: str, amount):
        """Create and persist a new transaction, then return it."""
        transaction = Transaction(account_id=account_id, txn_type=txn_type, amount=amount)
        db.add(transaction)
        # commit() makes the insert durable in the database; refresh() loads the generated primary key and any defaults back into the object.
        db.commit()
        db.refresh(transaction)
        return transaction

    def get_transactions_by_account(self, db: Session, account_id: int):
        """Return all transactions for an account in chronological order."""
        return db.query(Transaction).filter(Transaction.account_id == account_id).order_by(Transaction.created_at.asc()).all()

