import os
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
from config.system_prompt import generate_system_prompt

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOTENV_PATH = ".env" 

load_dotenv(dotenv_path=DOTENV_PATH)

ASSISTANT_NAME = os.getenv("ASSISTANT_NAME", "KYREN")
ASSISTANT_FULL_NAME = os.getenv(
	"ASSISTANT_FULL_NAME",
	"Knowledge-based Yielding Reasoning Executive Network",
)
LOG_DIR = Path(os.getenv("LOG_DIR", PROJECT_ROOT / "logs"))
LOG_FILE = LOG_DIR / f"{ASSISTANT_NAME.lower()}.log"


@dataclass(frozen=True)
class BrainConfig:
	api_key: str = os.getenv("GEMINI_API_KEY", "")
	model: str = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
	assistant_name: str = ASSISTANT_NAME
	assistant_full_name: str = ASSISTANT_FULL_NAME
	system_prompt: str = generate_system_prompt(ASSISTANT_NAME, ASSISTANT_FULL_NAME)
	timeout_s: float = float(os.getenv("GEMINI_TIMEOUT_S", "60"))
	max_retries: int = int(os.getenv("GEMINI_MAX_RETRIES", "2"))
