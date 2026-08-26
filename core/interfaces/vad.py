from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.audio import AudioChunk
from core.models.transcription import VADResult


class VoiceActivityDetector(ABC):
    """Stateful: process() is called once per incoming AudioChunk, in
    order, and internally tracks whether we're currently 'in speech' so
    it can report speech_started / speech_ended transitions."""

    @abstractmethod
    def process(self, audio: AudioChunk) -> VADResult:
        ...

    @abstractmethod
    def reset(self) -> None:
        """Clear internal state (call after an utterance completes)."""
