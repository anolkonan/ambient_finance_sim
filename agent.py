from langchain_core.messages import HumanMessage, SystemMessage
from banking_data import simulate_large_expense
from banking_data import risk_profile
from banking_data import calculate_monthly_spending
from banking_data import get_user_profile
from banking_data import calculate_financial_metrics
from banking_data import rule_engine
from banking_data import decision_confidence
from banking_data import simulate_savings_increase
from banking_data import dashboard_metrics

from banking_data import decision_confidence
from langchain_community.chat_message_histories import ChatMessageHistory
from llm_config import get_llm


import json

# Initialize memory
memory = ChatMessageHistory()

def ambient_agent(user_query, risk_mode="Balanced"):

    llm = get_llm()

    # Core Data
    spending = calculate_monthly_spending()
    profile = get_user_profile()
    metrics = calculate_financial_metrics()
    flags = rule_engine(metrics)
    scenario = simulate_large_expense(3000)
    confidence = decision_confidence(metrics)
    dashboard = dashboard_metrics()

    # Use UI-selected risk mode
    risk_data = risk_profile(metrics, mode=risk_mode)
    selected_risk_mode = risk_data["profile"]
    risk_mode = {
        "profile": selected_risk_mode,
        "tone": risk_data["tone"],
        "max_recommendation_score": risk_data["max_recommendation_score"]
    }

    system_prompt = """
You are an AI-powered personal finance assistant.

Rules:
- Provide practical and data-driven financial advice.
- Be structured and concise.
- Do not guarantee investment returns.
- Highlight risks clearly.
- Use previous conversation context when relevant.

Respond ONLY in valid JSON format:

{
  "financial_assessment": "...",
  "risk_level": "...",
  "recommendation": "Yes / No / Cautious Yes",
  "recommendation_score": 0-100,
  "confidence_level": "Low / Medium / High",
  "reasoning": ["point1", "point2", "point3"]
}

Do not include explanations outside the JSON.
"""

    user_context = f"""
User Financial Goal:
{profile.get('goal', 'Not specified')}

Monthly Financial Overview:
{spending}

Financial Metrics:
{metrics}

Rule Engine Flags:
{flags}

Risk Profile:
Mode: {risk_data['profile']}
Tone Guidance: {risk_data['tone']}
Max Recommendation Score Allowed: {risk_data['max_recommendation_score']}

Confidence Level:
{confidence}

Dashboard Metrics:
{dashboard}

User Question:
{user_query}

Scenario Simulation:
{scenario}
"""

    messages = [
        SystemMessage(content=system_prompt),
        *memory.messages,
        HumanMessage(content=user_context)
    ]

    response = llm.invoke(messages)

    try:
        parsed_response = json.loads(response.content)
    except json.JSONDecodeError:
        parsed_response = {
            "error": "Model did not return valid JSON",
            "raw_response": response.content
        }

    memory.add_user_message(user_query)
    memory.add_ai_message(response.content)

    return parsed_response