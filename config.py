"""Configuration loading and saving for the voice app."""

import json
import os
from pathlib import Path

CONFIG_FILE = Path(__file__).parent / "users.json"


def load_config() -> dict:
    """Load configuration from users.json."""
    if not CONFIG_FILE.exists():
        return {
            "users": {},
            "current_user": None,
            "api_key": os.environ.get("ELEVENLABS_API_KEY", ""),
        }

    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)

    # Allow environment variable to override stored API key
    if os.environ.get("ELEVENLABS_API_KEY"):
        config["api_key"] = os.environ["ELEVENLABS_API_KEY"]

    return config


def save_config(config: dict) -> None:
    """Save configuration to users.json."""
    # Don't save API key if it came from environment
    config_to_save = config.copy()
    if os.environ.get("ELEVENLABS_API_KEY"):
        config_to_save["api_key"] = ""

    with open(CONFIG_FILE, "w") as f:
        json.dump(config_to_save, f, indent=2)


def get_current_user(config: dict) -> dict | None:
    """Get the current user's configuration."""
    if not config.get("current_user"):
        return None
    return config["users"].get(config["current_user"])


def add_user(config: dict, user_id: str, voice_id: str, name: str) -> None:
    """Add a new user to the configuration."""
    config["users"][user_id] = {
        "voice_id": voice_id,
        "name": name,
    }
    if not config.get("current_user"):
        config["current_user"] = user_id
    save_config(config)


def switch_user(config: dict, user_id: str) -> bool:
    """Switch to a different user. Returns True if successful."""
    if user_id not in config["users"]:
        return False
    config["current_user"] = user_id
    save_config(config)
    return True


def list_users(config: dict) -> list[tuple[str, str, bool]]:
    """List all users. Returns list of (user_id, name, is_current)."""
    current = config.get("current_user")
    return [
        (uid, user["name"], uid == current)
        for uid, user in config["users"].items()
    ]
