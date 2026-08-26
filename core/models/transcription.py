from __future__ import annotations

from dataclasses import dataclass


@dataclass
class VADResult:
    is_speech: bool
    speech_started: bool
    speech_ended: bool
    probability: float = 0.0


@dataclass
class TranscriptionResult:
    text: str
    language: str | None
    duration: float          # length of the audio transcribed, seconds
    processing_time: float   # wall-clock time STT took, seconds

    @property
    def real_time_factor(self) -> float:
        if self.duration <= 0:
            return 0.0
        return self.processing_time / self.duration
