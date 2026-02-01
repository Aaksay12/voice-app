"""Cache manager for pre-cached audio files."""

import hashlib
from pathlib import Path

CACHE_DIR = Path(__file__).parent / "cache"


def get_cache_path(user_id: str, phrase: str) -> Path:
    """Get the cache file path for a user and phrase."""
    phrase_hash = hashlib.md5(phrase.encode()).hexdigest()
    return CACHE_DIR / user_id / f"{phrase_hash}.mp3"


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
    """List all cached file hashes for a user."""
    user_cache_dir = CACHE_DIR / user_id
    if not user_cache_dir.exists():
        return []
    return [f.stem for f in user_cache_dir.glob("*.mp3")]


def is_cached(user_id: str, phrase: str) -> bool:
    """Check if a phrase is cached for a user."""
    return get_cache_path(user_id, phrase).exists()
