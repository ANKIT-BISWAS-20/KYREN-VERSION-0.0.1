from __future__ import annotations

import time
from dataclasses import dataclass, field

import numpy as np


@dataclass
class AudioChunk:
    """A short slice of raw audio coming straight from the microphone."""

    samples: np.ndarray  # float32, shape (n_samples,), mono
    sample_rate: int
    channels: int
    timestamp: float = field(default_factory=time.time)

    @property
    def duration_s(self) -> float:
        return len(self.samples) / self.sample_rate


@dataclass
class AudioBuffer:
    """A complete assembled utterance, ready for STT."""

    samples: np.ndarray  # float32, shape (n_samples,), mono, 16kHz
    sample_rate: int

    @property
    def duration_s(self) -> float:
        return len(self.samples) / self.sample_rate


@dataclass
class AudioData:
    """Audio produced by TTS, ready for playback."""

    samples: np.ndarray  # float32, shape (n_samples,), mono
    sample_rate: int
    channels: int = 1

    @property
    def duration_s(self) -> float:
        return len(self.samples) / self.sample_rate
