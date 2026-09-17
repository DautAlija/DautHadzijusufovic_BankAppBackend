-- Simple Bank Application — Database Schema
-- PostgreSQL (Supabase)
-- Matches the SQLAlchemy models in models.py

-- USERS
-- A bank customer. Each user can own multiple accounts.
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ACCOUNTS
-- A bank account belonging to one user. Each account can have multiple transactions.
CREATE TABLE accounts (
    account_id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    balance NUMERIC(10, 2) DEFAULT 0,
    account_type VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- TRANSACTIONS
-- A single deposit or withdrawal against one account.
CREATE TABLE transactions (
    txn_id SERIAL PRIMARY KEY,
    account_id INTEGER NOT NULL,
    txn_type VARCHAR(20),
    amount NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES accounts(account_id)
);
