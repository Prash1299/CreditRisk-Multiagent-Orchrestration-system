from __future__ import annotations

import os

from core.config import get_settings


def llm_enabled() -> bool:
    settings = get_settings()
    return bool(settings.openai_api_key) and not os.getenv("PYTEST_CURRENT_TEST")


def get_chat_model():
    if not llm_enabled():
        return None
    from langchain_openai import ChatOpenAI

    settings = get_settings()
    return ChatOpenAI(
        model=settings.openai_model,
        api_key=settings.openai_api_key,
        temperature=0,
    )


def complete(system: str, user: str) -> str | None:
    model = get_chat_model()
    if model is None:
        return None
    from langchain_core.messages import HumanMessage, SystemMessage

    response = model.invoke([SystemMessage(content=system), HumanMessage(content=user)])
    return str(response.content)
