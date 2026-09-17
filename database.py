import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# The engine manages the shared connection pool used to communicate with Postgres.
engine = create_engine(DATABASE_URL)
# These settings let FastAPI route code control commits and flushes explicitly.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base collects table metadata from every model that inherits from it.
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        # yield lets FastAPI inject the session and continue here for cleanup after the request.
        yield db
    finally:
        db.close()
