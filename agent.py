from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from llm_config import get_llm


from banking_data import calculate_monthly_spending, get_user_profile
import os
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")

llm = get_llm()
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)

# Initialize memory
memory = ChatMessageHistory()


def ambient_agent(user_query):
    spending = calculate_monthly_spending()
    profile = get_user_profile()

    system_prompt = """
You are an AI-powered personal finance assistant.

Rules:
- Provide practical and data-driven financial advice.
- Be structured and concise.
- Do not guarantee investment returns.
- Highlight risks clearly.
- Use previous conversation context when relevant.
"""

    user_context = f"""
User Financial Goal:
{profile['goal']}

Monthly Financial Overview:
{spending}

User Question:
{user_query}
"""

    # Retrieve previous conversation history
    history = memory.messages

    messages = [
        SystemMessage(content=system_prompt),
        *history,
        HumanMessage(content=user_context)
    ]

    response = llm.invoke(messages)

    # Save conversation to memory
    memory.add_user_message(user_query)
    memory.add_ai_message(response.content)

    return response.content
