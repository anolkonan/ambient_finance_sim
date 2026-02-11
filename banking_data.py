import json
import os
from collections import defaultdict


def load_transactions():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "transactions.json")

    with open(file_path, "r") as file:
        data = json.load(file)
        return data["transactions"]


def load_user_profile():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(base_dir, "data", "user_profile.json")

    if not os.path.exists(file_path):
        return {}

    with open(file_path, "r") as file:
        content = file.read().strip()
        if not content:
            return {}
        return json.loads(content)



def calculate_monthly_spending():
    transactions = load_transactions()
    print(type(transactions))
    print(transactions)

    total_income = 0
    total_expenses = 0
    category_breakdown = defaultdict(float)

    for txn in transactions:
        if txn["type"] == "credit":
            total_income += txn["amount"]
        elif txn["type"] == "debit":
            total_expenses += txn["amount"]
            category_breakdown[txn["category"]] += txn["amount"]

    savings = total_income - total_expenses
    savings_rate = (savings / total_income) * 100 if total_income > 0 else 0
    expense_ratio = (total_expenses / total_income) * 100 if total_income > 0 else 0

    risk_score = calculate_risk_score(expense_ratio, savings_rate)

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings": savings,
        "savings_rate_percent": round(savings_rate, 2),
        "expense_ratio_percent": round(expense_ratio, 2),
        "category_breakdown": dict(category_breakdown),
        "risk_score": risk_score
    }


def calculate_risk_score(expense_ratio, savings_rate):
    if expense_ratio > 90:
        return "High Risk"
    elif expense_ratio > 70:
        return "Moderate Risk"
    elif savings_rate < 10:
        return "Low Stability"
    else:
        return "Financially Stable"


def get_user_profile():
    return load_user_profile()
