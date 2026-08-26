from __future__ import annotations

from dataclasses import dataclass


@dataclass
class BrainResponse:
    text: str
    input_tokens: int | None
    output_tokens: int | None
    latency: float  # seconds, request -> complete response
