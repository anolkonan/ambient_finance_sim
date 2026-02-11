from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from banking_data import calculate_monthly_spending, get_user_profile
import os
from dotenv import load_dotenv
load_dotenv()


llm = ChatOpenAI(model="gpt-4o-mini", temperature=0,api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")


def ambient_agent(user_query):
    spending = calculate_monthly_spending()
    profile = get_user_profile()

    context = f"""
You are a personal finance assistant.

User goal:
{profile['goal']}

Monthly spending summary:
{spending}

User question:
{user_query}
"""


    response = llm.invoke([HumanMessage(content=context)])
    return response.content
