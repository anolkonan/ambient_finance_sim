import os

USE_OPENAI = False  # Switch to True when you enable billing

def get_llm():
    if USE_OPENAI:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2,
            api_key=os.getenv("OPENAI_API_KEY")
        )
    else:
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            model="mistral",
            temperature=0.2
        )
