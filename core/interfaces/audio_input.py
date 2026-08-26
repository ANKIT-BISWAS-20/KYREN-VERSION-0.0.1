from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterator

from core.models.audio import AudioChunk


class AudioInput(ABC):
    """Abstraction over 'a thing that produces a stream of audio chunks'.

    Concrete implementations: infrastructure/audio/microphone.py (real),
    core/fakes.py FakeAudioInput (tests).
    """

    @abstractmethod
    def start(self) -> None:
        """Open the device / start capturing. Must be safe to call once."""

    @abstractmethod
    def read(self) -> AudioChunk:
        """Block until the next chunk is available and return it."""

    @abstractmethod
    def stop(self) -> None:
        """Release the device. Must be safe to call even if start() failed."""

    def chunks(self) -> Iterator[AudioChunk]:
        """Convenience generator: start() then yield read() forever."""
        self.start()
        try:
            while True:
                yield self.read()
        finally:
            self.stop()
