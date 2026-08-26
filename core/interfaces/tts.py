from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.audio import AudioData


class TextToSpeech(ABC):

    @abstractmethod
    def synthesize(self, text: str) -> AudioData:
        ...
