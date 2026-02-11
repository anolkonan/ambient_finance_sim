import os

USE_OPENAI = False  # 🔥 Switch this to True when you have quota

def get_llm():
    if USE_OPENAI:
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.2
        )
    else:
        # Local fallback using Ollama
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            model="mistral",
            temperature=0.2
        )


llm = get_llm()