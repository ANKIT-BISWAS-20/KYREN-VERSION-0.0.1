import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = Path(os.getenv("KYREN_LOG_DIR", PROJECT_ROOT / "logs"))
LOG_FILE = LOG_DIR / "kyren.log"
DOTENV_PATH = ".env" 

load_dotenv(dotenv_path=DOTENV_PATH)


@dataclass(frozen=True)
class BrainConfig:
	api_key: str = os.getenv("GEMINI_API_KEY", "")
	model: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
	system_prompt: str = os.getenv(
		"KYREN_SYSTEM_PROMPT", "You are KYREN, a helpful voice assistant."
	)
	timeout_s: float = float(os.getenv("GEMINI_TIMEOUT_S", "60"))
	max_retries: int = int(os.getenv("GEMINI_MAX_RETRIES", "2"))
