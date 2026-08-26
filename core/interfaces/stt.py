from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.audio import AudioBuffer
from core.models.transcription import TranscriptionResult


class SpeechToText(ABC):

    @abstractmethod
    def transcribe(self, audio: AudioBuffer) -> TranscriptionResult:
        ...
