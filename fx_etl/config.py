from pathlib import Path

# Folders
PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

# API settings
BASE_URL = "https://open.er-api.com/v6"
TIMEOUT_SECONDS = 20

# Ensure folders exist
RAW_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)