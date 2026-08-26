from __future__ import annotations

from abc import ABC, abstractmethod

from core.models.audio import AudioData


class AudioOutput(ABC):
    """Abstraction over 'a thing that plays audio out loud'.

    Deliberately separate from TextToSpeech: TTS produces AudioData,
    AudioOutput plays it. Neither knows about the other's internals.
    """

    @abstractmethod
    def play(self, audio: AudioData) -> None:
        """Play audio. May be blocking or non-blocking depending on impl;
        pipeline code should use is_playing() to poll rather than assume."""

    @abstractmethod
    def stop(self) -> None:
        """Stop playback immediately (used for interruption, Section 29)."""

    @abstractmethod
    def is_playing(self) -> bool:
        """Whether audio is currently being played."""
