import os
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOG_DIR = Path(os.getenv("JARVIS_LOG_DIR", PROJECT_ROOT / "logs"))
LOG_FILE = LOG_DIR / "jarvis.log"
