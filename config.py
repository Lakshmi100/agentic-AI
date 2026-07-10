# config.py
from pathlib import Path
from dotenv import load_dotenv
import os

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

LLM_PROVIDER  = os.getenv("LLM_PROVIDER", "claude")
ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
if not ANTHROPIC_KEY:
    raise RuntimeError("ANTHROPIC_API_KEY missing — check your .env")