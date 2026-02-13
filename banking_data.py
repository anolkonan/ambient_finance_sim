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

def calculate_financial_metrics():
    transactions = load_transactions()
    profile = get_user_profile()

    total_income = sum(t["amount"] for t in transactions if t["type"] == "credit")
    total_expense = sum(t["amount"] for t in transactions if t["type"] == "debit")

    savings = total_income - total_expense
    savings_rate = (savings / total_income) * 100 if total_income else 0

    emergency_fund_target = profile.get("savings_goal", 0)
    months_of_runway = savings / (total_expense / 30) if total_expense else 0

    return {
        "income": total_income,
        "expenses": total_expense,
        "savings": savings,
        "savings_rate": round(savings_rate, 2),
        "runway_days": round(months_of_runway, 1),
        "emergency_target": emergency_fund_target
    }

def evaluate_risk(metrics):
    if metrics["savings_rate"] < 10:
        return "High Risk"
    elif metrics["savings_rate"] < 25:
        return "Moderate Risk"
    else:
        return "Low Risk"

def simulate_large_expense(amount):
    metrics = calculate_financial_metrics()
    new_savings = metrics["savings"] - amount

    new_savings_rate = (new_savings / metrics["income"]) * 100 if metrics["income"] else 0

    return {
        "new_savings": new_savings,
        "new_savings_rate": round(new_savings_rate, 2)
    }

def format_spending_report(spending):
    report = (
        f"Total Income: ${spending['total_income']}\n"
        f"Total Expenses: ${spending['total_expenses']}\n"
        f"Savings: ${spending['savings']}\n"
        f"Savings Rate: {spending['savings_rate_percent']}%\n"
        f"Expense Ratio: {spending['expense_ratio_percent']}%\n"
        f"Risk Score: {spending['risk_score']}\n"
        "Category Breakdown:\n"
    )
    for category, amount in spending["category_breakdown"].items():
        report += f"  - {category}: ${amount}\n"
    return report


def build_decision_prompt(question=None, scenario_amount=None):
    metrics = calculate_financial_metrics()
    spending = calculate_monthly_spending()
    risk_level = evaluate_risk(metrics)
    profile = get_user_profile()

    scenario_data = None
    if scenario_amount:
        scenario_data = simulate_large_expense(scenario_amount)

    prompt = f"""
You are a professional financial decision assistant.

USER FINANCIAL METRICS:
Income: {metrics['income']}
Expenses: {metrics['expenses']}
Savings: {metrics['savings']}
Savings Rate: {metrics['savings_rate']}%
Runway (days): {metrics['runway_days']}
Emergency Fund Target: {metrics['emergency_target']}

RISK LEVEL:
{risk_level}

CATEGORY BREAKDOWN:
{spending['category_breakdown']}

USER PROFILE:
{profile}

"""

    if scenario_data:
        prompt += f"""
SCENARIO SIMULATION:
New Savings After Expense: {scenario_data['new_savings']}
New Savings Rate: {scenario_data['new_savings_rate']}%
"""

    if question:
        prompt += f"\nUSER QUESTION:\n{question}\n"

    prompt += """
Provide:
1. A short financial assessment
2. Risk implications
3. A clear recommendation (Yes / No / Cautious Yes)
4. Reasoning in 3-5 bullet points
"""

    return prompt


def decision_confidence(metrics):
    if metrics["savings_rate"] > 30:
        return "High Confidence"
    elif metrics["savings_rate"] > 15:
        return "Medium Confidence"
    else:
        return "Low Confidence"

def rule_engine(metrics):
    flags = []

    if metrics["savings_rate"] < 10:
        flags.append("CRITICAL_LOW_SAVINGS")

    if metrics["runway_days"] < 30:
        flags.append("LOW_RUNWAY")

    if metrics["expenses"] > metrics["income"]:
        flags.append("NEGATIVE_CASHFLOW")

    return flags

def simulate_savings_increase(percent_increase):
    metrics = calculate_financial_metrics()
    
    additional_savings = metrics["income"] * (percent_increase / 100)
    new_savings = metrics["savings"] + additional_savings
    
    new_savings_rate = (
        (new_savings / metrics["income"]) * 100
        if metrics["income"] else 0
    )

    return {
        "new_savings": new_savings,
        "new_savings_rate": round(new_savings_rate, 2)
    }

def simulate_large_expense(amount):
    metrics = calculate_financial_metrics()

    new_savings = metrics["savings"] - amount
    new_savings_rate = (
        (new_savings / metrics["income"]) * 100
        if metrics["income"] else 0
    )

    return {
        "new_savings": new_savings,
        "new_savings_rate": round(new_savings_rate, 2)
    }

def risk_profile(metrics, mode="Balanced"):

    profiles = {
        "Conservative": {
            "profile": "Conservative",
            "tone": "Prioritize capital preservation and low volatility.",
            "max_recommendation_score": 60
        },
        "Balanced": {
            "profile": "Balanced",
            "tone": "Seek moderate growth with controlled risk exposure.",
            "max_recommendation_score": 80
        },
        "Aggressive": {
            "profile": "Aggressive",
            "tone": "Focus on high growth opportunities and accept volatility.",
            "max_recommendation_score": 100
        }
    }

    return profiles.get(mode, profiles["Balanced"])

def dashboard_metrics():
    metrics = calculate_financial_metrics()

    burn_rate = metrics["expenses"] / 30 if metrics["expenses"] else 0
    runway_months = metrics["savings"] / metrics["expenses"] if metrics["expenses"] else 0

    return {
        "savings_rate": metrics["savings_rate"],
        "burn_rate_daily": round(burn_rate, 2),
        "runway_months": round(runway_months, 2)
    }

def main():
    spending = calculate_monthly_spending()
    print(format_spending_report(spending))

if __name__ == "__main__":
    main()
