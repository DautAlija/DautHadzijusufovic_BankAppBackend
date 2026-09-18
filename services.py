from decimal import Decimal

from fastapi import HTTPException
from sqlalchemy.orm import Session

from repositories import AccountRepository, TransactionRepository, UserRepository


class AccountService:
    def __init__(self):
        self.user_repository = UserRepository()
        self.account_repository = AccountRepository()
        self.transaction_repository = TransactionRepository()

    def create_account(self, db: Session, user_id: int, account_type: str, current_user):
        """Create and persist a new account for a user."""
        # Admins may create accounts for any user, but regular users can only create their own account.
        if current_user.role != 'admin' and user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail='Not authorized to access this account')
        return self.account_repository.create_account(db, user_id, account_type)

    def get_account(self, db: Session, account_id: int, current_user):
        """Return an account or raise a 404 if it does not exist."""
        account = self.account_repository.get_account_by_id(db, account_id)
        if account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        # Only admins can view other users' accounts; regular users must own the account they access.
        if current_user.role != 'admin' and account.user_id != current_user.user_id:
            raise HTTPException(status_code=403, detail='Not authorized to access this account')
        return account

    def get_transactions(self, db: Session, account_id: int, current_user):
        """Return all transactions for an account after confirming the account exists."""
        # The lookup is intentionally done before the query so the same 404 behavior is reused for missing accounts.
        self.get_account(db, account_id, current_user)
        return self.transaction_repository.get_transactions_by_account(db, account_id)

    def get_my_accounts(self, db: Session, current_user):
        """Return all accounts that belong to the currently logged-in user."""
        return self.account_repository.get_accounts_by_user(db, current_user.user_id)

    def deposit(self, db: Session, account_id: int, amount, current_user):
        """Deposit a valid amount into an account and record the transaction."""
        # account.balance is a Decimal from the Numeric column, so we convert the incoming value to Decimal before arithmetic.
        amount = Decimal(str(amount))
        # The service fetches the account through get_account() so the same 404 logic is reused before any validation.
        account = self.get_account(db, account_id, current_user)
        if amount <= 0:
            raise HTTPException(status_code=400, detail="amount must be greater than zero")

        new_balance = account.balance + amount
        updated_account = self.account_repository.update_balance(db, account, new_balance)
        self.transaction_repository.create_transaction(db, account_id, 'DEPOSIT', amount)
        return updated_account

    def withdraw(self, db: Session, account_id: int, amount, current_user):
        """Withdraw a valid amount from an account and record the transaction."""
        # account.balance is a Decimal from the Numeric column, so we convert the incoming value to Decimal before arithmetic.
        amount = Decimal(str(amount))
        # The service fetches the account through get_account() so the same 404 logic is reused before any validation.
        account = self.get_account(db, account_id, current_user)
        if amount <= 0:
            raise HTTPException(status_code=400, detail="amount must be greater than zero")
        if amount > account.balance:
            raise HTTPException(status_code=400, detail="amount exceeds the account balance")

        new_balance = account.balance - amount
        updated_account = self.account_repository.update_balance(db, account, new_balance)
        self.transaction_repository.create_transaction(db, account_id, 'WITHDRAW', amount)
        return updated_account
