from __future__ import annotations

import httpx

from pyquest.config import Settings
from pyquest.rag.interfaces import LlmClient


class OllamaLlmClient(LlmClient):
    """Local Ollama chat completion client."""

    def __init__(
        self,
        *,
        base_url: str = "http://127.0.0.1:11434",
        model: str = "llama3.2",
        timeout_seconds: float = 12.0,
    ) -> None:
        self._base_url = (base_url or "http://127.0.0.1:11434").rstrip("/")
        self._model = model or "llama3.2"
        self._timeout_seconds = timeout_seconds

    @property
    def provider_name(self) -> str:
        return f"ollama:{self._model}"

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "stream": False,
        }
        with httpx.Client(timeout=self._timeout_seconds) as client:
            resp = client.post(f"{self._base_url}/api/chat", json=payload)
            resp.raise_for_status()
            data = resp.json()
        message = data.get("message") or {}
        content = str(message.get("content") or "").strip()
        if not content:
            raise ValueError("Empty response returned from Ollama API")
        return content


class GeminiLlmClient(LlmClient):
    """Google Gemini generateContent REST client."""

    def __init__(
        self,
        *,
        api_key: str,
        model: str = "gemini-2.0-flash",
        timeout_seconds: float = 12.0,
    ) -> None:
        self._api_key = api_key
        self._model = model or "gemini-2.0-flash"
        self._timeout_seconds = timeout_seconds

    @property
    def provider_name(self) -> str:
        return f"gemini:{self._model}"

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self._api_key:
            raise ValueError("Missing API key for Gemini provider")
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self._model}:generateContent?key={self._api_key}"
        )
        payload = {
            "systemInstruction": {"parts": [{"text": system_prompt}]},
            "contents": [{"role": "user", "parts": [{"text": user_prompt}]}],
            "generationConfig": {"temperature": 0.2},
        }
        with httpx.Client(timeout=self._timeout_seconds) as client:
            resp = client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
        candidates = data.get("candidates") or []
        parts = ((candidates[0].get("content") or {}).get("parts") or []) if candidates else []
        text = "\n".join(str(p.get("text") or "") for p in parts).strip()
        if not text:
            raise ValueError("Empty response returned from Gemini API")
        return text


class OpenAICompatLlmClient(LlmClient):
    """OpenAI-compatible /v1/chat/completions REST client."""

    def __init__(
        self,
        *,
        base_url: str = "https://api.openai.com",
        api_key: str = "",
        model: str = "gpt-4o-mini",
        timeout_seconds: float = 12.0,
    ) -> None:
        self._base_url = (base_url or "https://api.openai.com").rstrip("/")
        self._api_key = api_key
        self._model = model or "gpt-4o-mini"
        self._timeout_seconds = timeout_seconds

    @property
    def provider_name(self) -> str:
        return f"openai_compat:{self._model}"

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        headers: dict[str, str] = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        payload = {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }
        with httpx.Client(timeout=self._timeout_seconds) as client:
            resp = client.post(f"{self._base_url}/v1/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
        choices = data.get("choices") or []
        msg = (choices[0].get("message") or {}) if choices else {}
        content = str(msg.get("content") or "").strip()
        if not content:
            raise ValueError("Empty response returned from OpenAI-compatible API")
        return content


def build_llm_client(settings: Settings) -> LlmClient | None:
    """Instantiate an LlmClient from Settings, or return None for offline mode."""
    provider = settings.llm_provider
    if provider == "offline":
        return None
    if provider == "ollama":
        return OllamaLlmClient(
            base_url=settings.llm_base_url or "http://127.0.0.1:11434",
            model=settings.llm_model or "llama3.2",
            timeout_seconds=settings.llm_timeout_seconds,
        )
    if provider == "gemini":
        return GeminiLlmClient(
            api_key=settings.llm_api_key,
            model=settings.llm_model or "gemini-2.0-flash",
            timeout_seconds=settings.llm_timeout_seconds,
        )
    if provider == "openai_compat":
        return OpenAICompatLlmClient(
            base_url=settings.llm_base_url or "https://api.openai.com",
            api_key=settings.llm_api_key,
            model=settings.llm_model or "gpt-4o-mini",
            timeout_seconds=settings.llm_timeout_seconds,
        )
    return None
