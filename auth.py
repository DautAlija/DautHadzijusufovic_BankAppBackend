# Import the bcrypt library directly for password hashing and verification.
import os
from datetime import datetime, timedelta

import bcrypt
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from database import get_db
from repositories import UserRepository

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = 'HS256'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/login')


# Hash a plain-text password before storing it in the database.
def hash_password(password: str):
    """Hash a plain-text password using the configured bcrypt scheme."""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


# Check whether a submitted password matches the stored bcrypt hash.
def verify_password(plain_password: str, hashed_password: str):
    """Verify that a plain-text password matches the stored bcrypt hash."""
    plain_password_bytes = plain_password.encode('utf-8')
    hashed_password_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(plain_password_bytes, hashed_password_bytes)


# Create a signed JWT by adding an expiration claim so the token expires after a set time.
def create_access_token(data: dict, expires_delta_minutes: int = 30):
    """Create a JWT payload containing the provided data and an exp claim that expires after the configured number of minutes."""
    to_encode = data.copy()
    expires = datetime.utcnow() + timedelta(minutes=expires_delta_minutes)
    to_encode['exp'] = expires
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# Decode a JWT and return the payload, or None if the token is expired or tampered with.
def decode_access_token(token: str):
    """Decode a JWT and return its payload; returns None if the token is expired, invalid, or tampered with."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        return None


# Validate the bearer token and resolve it to the authenticated user for protected routes.
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """Resolve the authenticated user from a valid bearer token so protected routes can reuse the same access check."""
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(status_code=401, detail='Invalid or expired token')

    email = payload.get('sub')
    if not email:
        raise HTTPException(status_code=401, detail='Invalid or expired token')

    user = UserRepository().get_user_by_email(db, email)
    if user is None:
        raise HTTPException(status_code=401, detail='Invalid or expired token')

    return user
