from pathlib import Path
import sqlite3

# -----------------------------
# PROJECT ROOT
# -----------------------------
# Get the project root directory (folder containing config.py)
PROJECT_ROOT = Path(__file__).resolve().parent

# -----------------------------
# DATA DIRECTORIES
# -----------------------------
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

# -----------------------------
# DATABASE PATH
# -----------------------------
DB_PATH = PROJECT_ROOT / "olist.db"

def get_connection():
    """Returns a new SQLite connection to the project database."""
    return sqlite3.connect(DB_PATH)

# -----------------------------
# PRINT PATHS (Optional Debug)
# -----------------------------
if __name__ == "__main__":
    print("Project Root:", PROJECT_ROOT)
    print("Raw Data Folder:", DATA_RAW)
    print("Processed Folder:", DATA_PROCESSED)
    print("Database Path:", DB_PATH)
