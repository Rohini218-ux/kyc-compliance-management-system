
from pathlib import Path

# Backend project directory
BASE_DIR = Path(__file__).resolve().parents[2]

# PDF storage directory
DOCUMENT_STORAGE_DIR = BASE_DIR / "storage" / "documents"

# Maximum upload size: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024

# Allowed file extension
ALLOWED_EXTENSION = ".pdf"

# Create storage directory automatically
DOCUMENT_STORAGE_DIR.mkdir(
    parents=True,
    exist_ok=True
)
