# Setup

## 0. Inspect your environment first

```bash
python --version     # or python3 --version
pip --version
git --version
```

Confirm which OS you're on — commands below diverge for Windows vs
Linux/macOS where noted.

## 1. Create and activate a virtual environment

Linux/macOS:
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

## 2. Install dependencies

```bash
pip install -r requirements.txt
```

### Per-dependency notes

**sounddevice** (audio I/O)
- Why: stable, cross-platform PortAudio wrapper.
- Source: https://python-sounddevice.readthedocs.io/
- Verify: `python -c "import sounddevice as sd; print(sd.query_devices())"`
- Linux: may require `libportaudio2` via your system package manager
  (`apt install libportaudio2` on Debian/Ubuntu) if the import fails.
- Windows: generally works out of the box (bundled PortAudio binary).

**faster-whisper** (local STT)
- Why: CTranslate2-based reimplementation of Whisper; fast CPU inference,
  supports INT8 quantization.
- Source: https://github.com/SYSTRAN/faster-whisper
- Verify: `python -c "from faster_whisper import WhisperModel; print('ok')"`
- Common error: first run downloads model weights — needs network access
  once; subsequent runs are cached locally (`~/.cache/huggingface`).

**silero-vad** (voice activity detection)
- Why: small, fast, accurate neural VAD; runs comfortably on CPU alongside
  Whisper.
- Source: https://github.com/snakers4/silero-vad
- Verify: `python -c "from silero_vad import load_silero_vad; load_silero_vad()"`
- **Check this before installing**: the project's packaging has changed;
  confirm the current PyPI package name and import path against the repo
  README rather than trusting this document blindly.

**openai** (reasoning)
- Why: official SDK, handles retries/timeouts.
- Source: https://github.com/openai/openai-python , docs at
  https://platform.openai.com/docs/
- Verify: `python -c "import openai; print(openai.__version__)"`
- Common error: `AuthenticationError` → check `OPENAI_API_KEY` in `.env`.

**kokoro** (local TTS)
- Why: fast, good-quality local TTS with no cloud dependency.
- Source: verify current authoritative repo before installing — commonly
  referenced at https://github.com/hexgrad/kokoro and
  https://huggingface.co/hexgrad/Kokoro-82M — **do not assume this is
  still current without checking**.
- Verify: `python -c "from kokoro import KPipeline; print('ok')"`
- Common error: missing `espeak-ng` system dependency for phonemization
  on some platforms — check the installed version's README for its
  current system-level requirements.

**torch** (required by faster-whisper's runtime and Silero VAD)
- CPU-only build is sufficient for Phase 1 (we are not using ROCm).
- Verify: `python -c "import torch; print(torch.__version__)"`

## 3. Configure environment variables

```bash
cp .env.example .env
```

Edit `.env` and set at minimum `OPENAI_API_KEY`. Never commit this file —
it's already in `.gitignore`.

## 4. List audio devices and pick the right one

```bash
python tests/test_microphone.py --list-devices
```

If the default device isn't what you want, set `AUDIO_INPUT_DEVICE` in
`.env` to the device index or name shown.

## 5. Smoke-test the microphone

```bash
python tests/test_microphone.py
```

Expected output: `OK: received N samples ...` after speaking for ~3s.

## 6. Run the test suite (all mocked, no hardware/API needed)

```bash
pytest tests/ -v
```

## 7. Run Jarvis

```bash
python main.py
```
