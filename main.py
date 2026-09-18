from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from auth import create_access_token, get_current_user, hash_password, verify_password
from database import get_db
from repositories import UserRepository
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


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


@app.post("/api/accounts")
def create_account(account: AccountRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Create a new account for the provided user."""
    return account_service.create_account(db, account.userId, account.accountType, current_user)


@app.get("/api/accounts/{account_id}")
def get_account(account_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Return the matching account by ID."""
    return account_service.get_account(db, account_id, current_user)


@app.post("/api/accounts/{account_id}/deposit")
def deposit_to_account(account_id: int, deposit: DepositRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Deposit a valid amount into the selected account."""
    return account_service.deposit(db, account_id, deposit.amount, current_user)


@app.post("/api/accounts/{account_id}/withdraw")
def withdraw_from_account(account_id: int, withdrawal: DepositRequest, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Withdraw a valid amount from the selected account."""
    return account_service.withdraw(db, account_id, withdrawal.amount, current_user)


@app.get("/api/accounts/{account_id}/transactions")
def get_account_transactions(account_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Return all transactions for the selected account."""
    return account_service.get_transactions(db, account_id, current_user)


@app.get("/api/my-accounts")
def get_my_accounts(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """Return all accounts belonging to the currently authenticated user."""
    return account_service.get_my_accounts(db, current_user)


@app.post("/api/register")
def register_user(register: RegisterRequest, db: Session = Depends(get_db)):
    """Register a new user after checking for duplicate emails and hashing the password."""
    user_repository = UserRepository()

    existing_user = user_repository.get_user_by_email(db, register.email)
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    hashed_password = hash_password(register.password)
    created_user = user_repository.create_user(db, register.name, register.email, hashed_password)

    return {
        'user_id': created_user.user_id,
        'name': created_user.name,
        'email': created_user.email,
        'created_at': created_user.created_at,
        'role': created_user.role,
    }


@app.post("/api/login")
def login_user(login: LoginRequest, db: Session = Depends(get_db)):
    """Authenticate a user and return a JWT access token for valid credentials."""
    user_repository = UserRepository()
    user = user_repository.get_user_by_email(db, login.email)

    # We use one generic 401 error to avoid revealing whether the email or password was wrong.
    if not user or not verify_password(login.password, user.password):
        raise HTTPException(status_code=401, detail='Invalid credentials')

    token = create_access_token({'sub': user.email, 'role': user.role})
    return {'access_token': token, 'token_type': 'bearer'}


@app.get("/api/me")
def get_current_user_profile(current_user=Depends(get_current_user)):
    """Return the authenticated user's profile details."""
    return {
        'user_id': current_user.user_id,
        'name': current_user.name,
        'email': current_user.email,
        'role': current_user.role,
    }