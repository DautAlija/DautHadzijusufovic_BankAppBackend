# FastAPI imports: provide the web app class and the standard HTTP error response.
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
# Date utility: provides today's date for each transaction record.
from datetime import date

# FastAPI application object: receives route registrations and serves the API.
app = FastAPI()

accounts = []
next_account_id = 1
transactions = []
next_txn_id = 1


# Pydantic model: describes and validates the JSON body FastAPI should accept.
class AccountRequest(BaseModel):
	# Type hint: requires userId to be provided as an integer in the JSON body.
	userId: int
	# Type hint: requires accountType to be provided as a string in the JSON body.
	accountType: str


# Pydantic model: describes and validates the JSON body for a deposit request.
class DepositRequest(BaseModel):
	# Type hint: requires amount to be provided as a number in the JSON body.
	amount: float


def find_account(account_id):
	"""Find an account by ID or raise a 404 error if it does not exist."""
	for account in accounts:
		if account["accountId"] == account_id:
			return account

	# HTTPException: provides the same clear HTTP 404 response for every account lookup.
	raise HTTPException(status_code=404, detail="Account not found")


# FastAPI decorator: registers this function as the handler for POST /api/accounts.
@app.post("/api/accounts")
# Type hint: tells FastAPI to parse the request body into the Pydantic model.
def create_account(account: AccountRequest):
	"""Create an in-memory bank account with a generated ID and zero balance."""
	global next_account_id

	if account.userId <= 0:
		# FastAPI exception: sends a clear HTTP 400 validation error to the client.
		raise HTTPException(status_code=400, detail="userId must be a positive number")

	if not account.accountType.strip():
		# FastAPI exception: sends a clear HTTP 400 validation error to the client.
		raise HTTPException(status_code=400, detail="accountType must not be empty")

	created_account = {
		"accountId": next_account_id,
		"userId": account.userId,
		"accountType": account.accountType,
		"balance": 0,
	}
	accounts.append(created_account)
	next_account_id += 1

	return created_account


# FastAPI decorator: registers this function as the handler for GET /api/accounts/{account_id}.
@app.get("/api/accounts/{account_id}")
# Type hint: tells FastAPI to parse the account_id path value as an integer.
def get_account(account_id: int):
	"""Return the in-memory account that matches the requested ID."""
	return find_account(account_id)


# FastAPI decorator: registers this function as the handler for GET /api/accounts/{account_id}/transactions.
@app.get("/api/accounts/{account_id}/transactions")
# Type hint: tells FastAPI to parse the account_id path value as an integer.
def get_account_transactions(account_id: int):
	"""Return all transactions associated with the requested account."""
	find_account(account_id)
	return [transaction for transaction in transactions if transaction["accountId"] == account_id]


# FastAPI decorator: registers this function as the handler for POST /api/accounts/{account_id}/withdraw.
@app.post("/api/accounts/{account_id}/withdraw")
# Type hint: tells FastAPI to parse the account_id path value as an integer.
# Type hint: tells FastAPI to parse the request body into the Pydantic deposit model.
def withdraw_from_account(account_id: int, withdrawal: DepositRequest):
	"""Withdraw a valid amount from the matching in-memory account."""
	global next_txn_id

	account = find_account(account_id)
	if withdrawal.amount <= 0:
		# FastAPI exception: sends a clear HTTP 400 response for invalid withdrawals.
		raise HTTPException(status_code=400, detail="amount must be greater than zero")

	if withdrawal.amount > account["balance"]:
		# FastAPI exception: sends a clear HTTP 400 response when funds are insufficient.
		raise HTTPException(status_code=400, detail="amount exceeds the account balance")

	account["balance"] -= withdrawal.amount
	transactions.append({
		"txnId": next_txn_id,
		"accountId": account_id,
		"txnType": "WITHDRAW",
		"amount": withdrawal.amount,
		# ISO format stores today's date as a consistent YYYY-MM-DD string.
		"date": date.today().isoformat(),
	})
	next_txn_id += 1
	return account


# FastAPI decorator: registers this function as the handler for POST /api/accounts/{account_id}/deposit.
@app.post("/api/accounts/{account_id}/deposit")
# Type hint: tells FastAPI to parse the account_id path value as an integer.
# Type hint: tells FastAPI to parse the request body into the Pydantic deposit model.
def deposit_to_account(account_id: int, deposit: DepositRequest):
	"""Deposit a positive amount into the matching in-memory account."""
	global next_txn_id

	account = find_account(account_id)
	if deposit.amount <= 0:
		# FastAPI exception: sends a clear HTTP 400 response for invalid deposits.
		raise HTTPException(status_code=400, detail="amount must be greater than zero")

	account["balance"] += deposit.amount
	transactions.append({
		"txnId": next_txn_id,
		"accountId": account_id,
		"txnType": "DEPOSIT",
		"amount": deposit.amount,
		# ISO format stores today's date as a consistent YYYY-MM-DD string.
		"date": date.today().isoformat(),
	})
	next_txn_id += 1
	return account