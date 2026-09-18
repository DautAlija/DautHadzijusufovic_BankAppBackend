from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db
from services import AccountService

# The React frontend runs on a different port than the API, and browsers block cross-origin requests by default.
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:5173'],
    allow_methods=['*'],
    allow_headers=['*'],
)
account_service = AccountService()


class AccountRequest(BaseModel):
    userId: int
    accountType: str


class DepositRequest(BaseModel):
    amount: float


@app.post("/api/accounts")
def create_account(account: AccountRequest, db: Session = Depends(get_db)):
    """Create a new account for the provided user."""
    return account_service.create_account(db, account.userId, account.accountType)


@app.get("/api/accounts/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db)):
    """Return the matching account by ID."""
    return account_service.get_account(db, account_id)


@app.post("/api/accounts/{account_id}/deposit")
def deposit_to_account(account_id: int, deposit: DepositRequest, db: Session = Depends(get_db)):
    """Deposit a valid amount into the selected account."""
    return account_service.deposit(db, account_id, deposit.amount)


@app.post("/api/accounts/{account_id}/withdraw")
def withdraw_from_account(account_id: int, withdrawal: DepositRequest, db: Session = Depends(get_db)):
    """Withdraw a valid amount from the selected account."""
    return account_service.withdraw(db, account_id, withdrawal.amount)


@app.get("/api/accounts/{account_id}/transactions")
def get_account_transactions(account_id: int, db: Session = Depends(get_db)):
    """Return all transactions for the selected account."""
    return account_service.get_transactions(db, account_id)