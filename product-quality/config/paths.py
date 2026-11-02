"""Filesystem paths."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
SQL_DIR = ROOT / "sql"
CATEGORY_CHART = DATA_DIR / "category_on_time.png"
