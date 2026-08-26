from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator

from core.models.messages import Message
from core.models.responses import BrainResponse


class Brain(ABC):

    @abstractmethod
    def generate(self, messages: list[Message]) -> BrainResponse:
        ...

    def generate_stream(self, messages: list[Message]) -> Iterator[str]:
        """Optional: yield text chunks as they arrive. Default
        implementation falls back to non-streaming for brains that
        don't support it, so the pipeline can always call this safely."""
        result = self.generate(messages)
        yield result.text
