from langchain_openai import ChatOpenAI

from config import (
    LLM_API_KEY,
    LLM_BASE_URL,
    LLM_MODEL,
)


def get_llm(temperature: float = 0):
    """
    Retourne le modèle LLM configuré pour le projet.
    """

    return ChatOpenAI(
        model=LLM_MODEL,
        api_key=LLM_API_KEY,
        base_url=LLM_BASE_URL,
        temperature=temperature,
    )