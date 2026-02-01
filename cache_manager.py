"""Cache manager for pre-cached audio files."""

import re
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"
MAX_FILENAME_LENGTH = 100


def sanitize_phrase(phrase: str) -> str:
    """Convert phrase to a safe filename (no punctuation, lowercase, underscores)."""
    # Remove punctuation and convert to lowercase
    sanitized = re.sub(r'[^\w\s]', '', phrase.lower())
    # Replace whitespace with underscores
    sanitized = re.sub(r'\s+', '_', sanitized.strip())
    # Limit length
    if len(sanitized) > MAX_FILENAME_LENGTH:
        sanitized = sanitized[:MAX_FILENAME_LENGTH]
    return sanitized


def get_cache_path(user_id: str, phrase: str) -> Path:
    """Get the cache file path for a user and phrase."""
    filename = sanitize_phrase(phrase)
    return CACHE_DIR / user_id / f"{filename}.mp3"


def get_cached_audio(user_id: str, phrase: str) -> bytes | None:
    """Get cached audio for a phrase. Returns None if not cached."""
    cache_path = get_cache_path(user_id, phrase)
    if cache_path.exists():
        return cache_path.read_bytes()
    return None


def save_to_cache(user_id: str, phrase: str, audio_data: bytes) -> Path:
    """Save audio data to cache. Returns the cache path."""
    cache_path = get_cache_path(user_id, phrase)
    cache_path.parent.mkdir(parents=True, exist_ok=True)
    cache_path.write_bytes(audio_data)
    return cache_path


def list_cached_phrases(user_id: str) -> list[str]:
    """List all cached phrase names for a user."""
    user_cache_dir = CACHE_DIR / user_id
    if not user_cache_dir.exists():
        return []
    return sorted([f.stem for f in user_cache_dir.glob("*.mp3")])


def is_cached(user_id: str, phrase: str) -> bool:
    """Check if a phrase is cached for a user."""
    return get_cache_path(user_id, phrase).exists()


def delete_from_cache(user_id: str, phrase: str) -> bool:
    """Delete a phrase from cache. Returns True if deleted, False if not found."""
    cache_path = get_cache_path(user_id, phrase)
    if cache_path.exists():
        cache_path.unlink()
        return True
    return False


def delete_from_cache_by_name(user_id: str, filename: str) -> bool:
    """Delete a cache file by its sanitized name. Returns True if deleted."""
    cache_path = CACHE_DIR / user_id / f"{filename}.mp3"
    if cache_path.exists():
        cache_path.unlink()
        return True
    return False
