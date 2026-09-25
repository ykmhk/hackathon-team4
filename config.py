"""Application configuration loaded from local environment variables."""

from os import environ
from pathlib import Path

from dotenv import load_dotenv


# config.py is in the repository root, so this loads the root-level .env file.
load_dotenv(Path(__file__).resolve().parent / ".env")


def _read_bool(name: str, default: bool = False) -> bool:
    """Convert an environment-variable string into a real Boolean value."""
    value = environ.get(name, str(default))
    return value.lower() in {"1", "true", "yes", "on"}


class Config:
    """Configuration used when the application runs normally."""

    SECRET_KEY = environ.get("SECRET_KEY")
    WTF_CSRF_SECRET_KEY = environ.get("WTF_CSRF_SECRET_KEY")
    TESTING = _read_bool("TESTING")