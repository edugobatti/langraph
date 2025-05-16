"""
Global settings for the SIEG AI project.
"""
import os
import pathlib
from dotenv import load_dotenv

# Base paths
BASE_DIR = pathlib.Path(__file__).parent.parent
FILES = BASE_DIR / "files"


# Load environment variables
env_path = BASE_DIR / "config" / ".env"
load_dotenv()

# API Keys and Port
OPENAI_API_KEY = os.getenv("OPENAI_KEY", "")
MODEL=os.getenv("MODEL")
PORT = int(os.getenv("PORT",5000))


# Data files paths
AGENTS_FILE = FILES / "agents.json"