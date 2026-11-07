import json
import logging
from typing import Iterator

from backend.app.config import settings

logger = logging.getLogger("rag.llm")


def _get_ollama_client():
    import ollama

    if settings.LLM_BASE_URL:
        return ollama.Client(host=settings.LLM_BASE_URL)
    return ollama.Client()


def _get_openai_client():
    import openai

    base_url = settings.LLM_BASE_URL.strip() if settings.LLM_BASE_URL else None
    return openai.OpenAI(
        api_key=settings.LLM_API_KEY or "dummy-key",
        base_url=base_url,
    )


def chatStream(messages: list[dict]) -> Iterator[str]:
    """Yields text tokens from the configured LLM provider."""
    provider = settings.LLM_PROVIDER.lower()
    if provider == "ollama":
        client = _get_ollama_client()
        response = client.chat(
            model=settings.LLM_MODEL,
            messages=messages,
            stream=True,
        )
        for chunk in response:
            content = chunk.get("message", {}).get("content", "")
            if content:
                yield content

    elif provider == "openai":
        client = _get_openai_client()
        stream = client.chat.completions.create(
            model=settings.LLM_MODEL,
            messages=messages,
            stream=True,
        )
        for chunk in stream:
            if chunk.choices and chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")


def chatJson(messages: list[dict], schema: dict, temperature: float = 0.3, maxTokens: int = 600) -> str:
    """Returns JSON text from the configured LLM provider matching the given schema."""
    provider = settings.LLM_PROVIDER.lower()
    if provider == "ollama":
        client = _get_ollama_client()
        response = client.chat(
            model=settings.LLM_MODEL,
            messages=messages,
            format=schema,
            options={"temperature": temperature, "num_predict": maxTokens},
        )
        return response.get("message", {}).get("content", "{}")

    elif provider == "openai":
        client = _get_openai_client()
        augmented_messages = list(messages)
        schema_desc = f"\nPlease respond in valid JSON format matching: {json.dumps(schema)}"
        if augmented_messages and augmented_messages[0].get("role") == "system":
            first = dict(augmented_messages[0])
            first["content"] = first["content"] + schema_desc
            augmented_messages[0] = first
        else:
            augmented_messages.insert(0, {"role": "system", "content": schema_desc})

        kwargs: dict = {
            "model": settings.LLM_MODEL,
            "messages": augmented_messages,
            "temperature": temperature,
            "max_tokens": maxTokens,
        }
        try:
            res = client.chat.completions.create(
                **kwargs,
                response_format={"type": "json_object"},
            )
            if res.choices and res.choices[0].message.content:
                return res.choices[0].message.content
        except Exception:
            try:
                res = client.chat.completions.create(**kwargs)
                if res.choices and res.choices[0].message.content:
                    return res.choices[0].message.content
            except Exception as e2:
                logger.warning("chatJson fallback error: %s", e2)
        return "{}"

    else:
        raise ValueError(f"Unsupported LLM provider: {settings.LLM_PROVIDER}")

