from pathlib import Path


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# Application settings
PROJECT_NAME = "Nexus Supply Chain Intelligence"
VERSION = "0.1.0"