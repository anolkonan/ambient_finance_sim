import json

def load_transactions():
    with open("data/transactions.json") as f:
        return json.load(f)

def calculate_monthly_spending():
    transactions = load_transactions()
    total = sum(t["amount"] for t in transactions if t["type"] == "debit")
    return total

def get_user_profile():
    with open("data/user_profile.json") as f:
        return json.load(f)
