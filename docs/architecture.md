# Architecture

## Diagram

```
                          KYREN
                           │
                     ┌─────┴─────┐
                     │  Pipeline │
                     └─────┬─────┘
                           │
        ┌──────────────────┼──────────────────┐
        ↓                  ↓                  ↓
      INPUT              BRAIN              OUTPUT
        │                  │                  │
  Microphone           Gemini              TTS
        │                  │                  │
       VAD                 │               Kokoro
        │                  │                  │
     Buffer                │              Audio Out
        │                  │                  │
      Whisper ─────────────┘                  │
        │                                     │
        └─────────────────────────────────────┘
```

Future phases (memory, tools, planner, vision) attach without requiring a
rewrite of this I/O layer — see Section 39 of the master prompt and
`docs/decisions.md`.

## Module responsibilities

| Module | Responsibility |
|---|---|
| `core/interfaces/` | Abstract contracts only. No implementation logic. |
| `core/models/` | Plain dataclasses passed between stages (`AudioChunk`, `AudioBuffer`, `AudioData`, `TranscriptionResult`, `VADResult`, `Message`, `BrainResponse`). |
| `core/fakes.py` | Fake implementations of every interface, used in tests instead of real hardware/APIs. |
| `core/utterance_buffer.py` | Assembles a stream of chunks + VAD results into one complete utterance, handling pre-roll/post-roll. |
| `core/pipeline.py` | Wires everything together; the only place that knows the *order* of operations, not the *implementations*. |
| `infrastructure/audio/microphone.py` | Real mic capture via `sounddevice`. |
| `infrastructure/audio/speaker.py` | Real playback via `sounddevice`, decoupled from TTS. |
| `infrastructure/vad/silero.py` | Real VAD via Silero, converts raw probabilities into speech-start/end transitions using configured timing thresholds. |
| `infrastructure/stt/faster_whisper.py` | Real STT. Loads the model once in `__init__`, never per-call. |
| `infrastructure/brain/gemini.py` | Real reasoning via Google Gen AI SDK. Owns retry/timeout/error classification. |
| `infrastructure/tts/kokoro.py` | Real speech synthesis via Kokoro. Loads the model once. |
| `config/settings.py` | Single source of truth for every tunable constant. Nothing elsewhere hardcodes `"base"`, `"cpu"`, `"int8"`, `16000`, etc. |

## Why interfaces (Principles 1 & 2)

`core/pipeline.py` depends only on `core/interfaces/*`. It never imports
`WhisperModel`, `genai.Client(...)`, or `KPipeline` directly. This means:

- Tests run against `core/fakes.py` implementations — no microphone,
  no API key, no GPU/CPU-heavy model loads, and they run in milliseconds.
- Swapping `FasterWhisperSTT` for a different STT engine later touches
  exactly one file (`main.py`'s `build_pipeline()`), not the pipeline
  logic itself.
- Developer A and Developer B (Section 33) can each build and test their
  half against fakes for the other half, without blocking on each other.

## Data flow through one turn

1. `Microphone.read()` → `AudioChunk`
2. `SileroVAD.process(chunk)` → `VADResult` (is_speech, speech_started, speech_ended)
3. `UtteranceBuffer.add(chunk, vad_result)` → `None` until an utterance completes, then `AudioBuffer`
4. `FasterWhisperSTT.transcribe(buffer)` → `TranscriptionResult`
5. `GeminiBrain.generate(history)` → `BrainResponse`
6. `KokoroTTS.synthesize(response.text)` → `AudioData`
7. `Speaker.play(audio_data)` → sound out

Each arrow is a call across an interface boundary; nothing on either side
of an arrow needs to know the concrete type on the other side.
