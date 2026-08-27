"""Gemini brain implementation."""
from __future__ import annotations

import time
from typing import Iterator

from config.settings import BrainConfig
from core.interfaces.brain import Brain
from core.models.messages import Message
from core.models.responses import BrainResponse


class BrainError(RuntimeError):
    pass


class GeminiBrain(Brain):
    def __init__(self, config: BrainConfig):
        try:
            from google import genai
            from google.genai import types
        except ImportError as exc:
            raise BrainError(
                "The google-genai package is not installed. Run: "
                "pip install -r requirements.txt"
            ) from exc

        if not config.api_key:
            raise BrainError(
                "GEMINI_API_KEY is not set. Add it to your .env file "
                "(see .env.example) -- never hardcode it in source."
            )

        self._config = config
        self._types = types
        self._client = genai.Client(
            api_key=config.api_key,
            http_options=types.HttpOptions(
                timeout=int(config.timeout_s * 1000),
                retry_options=types.HttpRetryOptions(attempts=config.max_retries),
            ),
        )

    @staticmethod
    def _to_gemini_contents(messages: list[Message]) -> list[dict]:
        return [
            {
                "role": "model" if message.role == "assistant" else "user",
                "parts": [{"text": message.content}],
            }
            for message in messages
            if message.role != "system"
        ]

    def _request_config(self):
        return self._types.GenerateContentConfig(
            system_instruction=self._config.system_prompt
        )

    def generate(self, messages: list[Message]) -> BrainResponse:
        start = time.perf_counter()
        try:
            response = self._client.models.generate_content(
                model=self._config.model,
                contents=self._to_gemini_contents(messages),
                config=self._request_config(),
            )
        except Exception as exc:
            raise BrainError(self._classify_error(exc)) from exc
        latency = time.perf_counter() - start

        usage = response.usage_metadata
        return BrainResponse(
            text=response.text or "",
            input_tokens=usage.prompt_token_count if usage else None,
            output_tokens=usage.candidates_token_count if usage else None,
            latency=latency,
        )

    def generate_stream(self, messages: list[Message]) -> Iterator[str]:
        try:
            stream = self._client.models.generate_content_stream(
                model=self._config.model,
                contents=self._to_gemini_contents(messages),
                config=self._request_config(),
            )
            for chunk in stream:
                if chunk.text:
                    yield chunk.text
        except Exception as exc:
            raise BrainError(self._classify_error(exc)) from exc

    def _classify_error(self, exc: Exception) -> str:
        assistant_name = self._config.assistant_name
        name = type(exc).__name__
        if "Timeout" in name:
            return f"{assistant_name} request timed out. Check your network connection."
        if "Authentication" in name or "Permission" in name:
            return f"{assistant_name} authentication failed. Check GEMINI_API_KEY in .env."
        if "ResourceExhausted" in name or "RateLimit" in name:
            return f"{assistant_name} rate limit hit. Please wait a moment and try again."
        if "Connection" in name:
            return f"Could not connect to {assistant_name}. Check your network connection."
        return f"{assistant_name} error: {exc}"
