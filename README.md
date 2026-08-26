# Jarvis — Phase 1

Local voice assistant pipeline:

```
🎤 Microphone → VAD → Whisper (CPU/INT8) → OpenAI → Kokoro TTS → 🔊 Speaker
```

Say something like *"Jarvis, explain what Docker is"* and it transcribes
your speech locally, sends it to the OpenAI API for reasoning, and speaks
the response back to you locally.

## Status

Phase 1 scope only. No memory, no tools, no agents, no vision — see
`docs/decisions.md` for what's explicitly deferred to later phases.

## Architecture

See `docs/architecture.md` for the full diagram and module responsibilities.
In short: everything depends on interfaces (`core/interfaces/`), not
concrete classes, so any component (STT, Brain, TTS, ...) can be swapped
without touching the pipeline.

## Installation

See `docs/setup.md` for exact, OS-specific commands. Summary:

```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env           # then fill in OPENAI_API_KEY
```

**Before installing, verify current versions/APIs** for `faster-whisper`,
`silero-vad`, `openai`, and especially `kokoro` (its packaging has moved
more than once) — see the source links in `docs/setup.md`.

## Running

```bash
python main.py
```

List audio input devices first if the wrong microphone gets picked:

```bash
python tests/test_microphone.py --list-devices
```

## Testing

```bash
pytest tests/                      # unit + component + integration (all mocked)
python tests/test_microphone.py    # real hardware smoke test
```

## Benchmarking

```bash
python scripts/benchmark_stt.py --audio-dir path/to/wav_files
python scripts/benchmark_pipeline.py --turns 10
```

See `docs/benchmarking.md` for methodology and how to interpret results.

## Project structure

```
jarvis/
├── main.py
├── core/
│   ├── interfaces/       # abstract contracts (AudioInput, VAD, STT, Brain, TTS, AudioOutput)
│   ├── models/           # dataclasses: AudioChunk, AudioBuffer, AudioData, TranscriptionResult, ...
│   ├── fakes.py          # Fake* implementations of every interface, for testing
│   ├── utterance_buffer.py
│   └── pipeline.py
├── infrastructure/
│   ├── audio/            # Microphone, Speaker (sounddevice)
│   ├── vad/              # SileroVAD
│   ├── stt/              # FasterWhisperSTT
│   ├── brain/            # OpenAIBrain
│   └── tts/              # KokoroTTS
├── config/settings.py    # all tunable constants, loaded from .env
├── tests/                # pytest unit/component/integration tests + hardware smoke test
├── scripts/               # benchmark_stt.py, benchmark_pipeline.py
└── docs/
```

## Troubleshooting

| Symptom | Likely cause | Check |
|---|---|---|
| `Could not access microphone` | Wrong/missing device, OS permissions | `python tests/test_microphone.py --list-devices` |
| `OPENAI_API_KEY is not set` | `.env` missing or not filled in | `cat .env` (don't share output) |
| OpenAI `AuthenticationError` | Invalid/expired key | Regenerate key on platform.openai.com |
| Import error on `kokoro` / `silero_vad` | Package not installed or renamed | `pip show kokoro`, check `docs/setup.md` links |
| STT very slow (RTF > 1) | Too many CPU threads competing, or `small` model expected | Lower `STT_CPU_THREADS`, confirm `STT_MODEL=base` |
