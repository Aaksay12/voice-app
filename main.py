#!/usr/bin/env python3
"""CLI entry point for the Eleven Labs Voice App."""

import sys

from audio_player import AudioPlayer
from cache_manager import get_cached_audio, is_cached, list_cached_phrases, save_to_cache
from config import (
    add_user,
    get_current_user,
    list_users,
    load_config,
    switch_user,
)
from tts_client import TTSClient


def print_help():
    """Print help message."""
    print("""
Eleven Labs Voice App
=====================
Type text to speak it using TTS.

Commands:
  /user <id>                  - Switch to user
  /users                      - List all users
  /add <id> <voice_id> <name> - Add a new user
  /cache <phrase>             - Pre-cache a phrase
  /list-cache                 - List cached phrases for current user
  /help                       - Show this help
  /quit                       - Exit
""")


def main():
    config = load_config()

    if not config.get("api_key"):
        print("Error: ELEVENLABS_API_KEY environment variable not set")
        sys.exit(1)

    tts_client = TTSClient(config["api_key"])
    player = AudioPlayer()

    print("Eleven Labs Voice App")
    print("Type /help for commands, /quit to exit")
    print()

    current_user = get_current_user(config)
    if current_user:
        print(f"Current user: {current_user['name']}")
    else:
        print("No user configured. Use /add to create one.")

    try:
        while True:
            try:
                text = input("> ").strip()
            except EOFError:
                break

            if not text:
                continue

            # Handle commands
            if text.startswith("/"):
                parts = text.split(maxsplit=1)
                cmd = parts[0].lower()
                args = parts[1] if len(parts) > 1 else ""

                if cmd == "/quit":
                    break

                elif cmd == "/help":
                    print_help()

                elif cmd == "/users":
                    users = list_users(config)
                    if not users:
                        print("No users configured.")
                    else:
                        print("Users:")
                        for uid, name, is_current in users:
                            marker = " *" if is_current else ""
                            print(f"  {uid}: {name}{marker}")

                elif cmd == "/user":
                    if not args:
                        print("Usage: /user <id>")
                    elif switch_user(config, args):
                        current_user = get_current_user(config)
                        print(f"Switched to user: {current_user['name']}")
                    else:
                        print(f"User '{args}' not found.")

                elif cmd == "/add":
                    add_parts = args.split(maxsplit=2)
                    if len(add_parts) < 3:
                        print("Usage: /add <id> <voice_id> <name>")
                    else:
                        uid, voice_id, name = add_parts
                        add_user(config, uid, voice_id, name)
                        current_user = get_current_user(config)
                        print(f"Added user: {name}")

                elif cmd == "/cache":
                    if not args:
                        print("Usage: /cache <phrase>")
                    elif not current_user:
                        print("No user selected. Use /add or /user first.")
                    else:
                        user_id = config["current_user"]
                        if is_cached(user_id, args):
                            print("Phrase already cached.")
                        else:
                            print("Caching phrase...")
                            try:
                                audio = tts_client.text_to_speech(
                                    args, current_user["voice_id"]
                                )
                                save_to_cache(user_id, args, audio)
                                print("Phrase cached successfully.")
                            except Exception as e:
                                print(f"Error caching phrase: {e}")

                elif cmd == "/list-cache":
                    if not current_user:
                        print("No user selected.")
                    else:
                        hashes = list_cached_phrases(config["current_user"])
                        if not hashes:
                            print("No cached phrases.")
                        else:
                            print(f"Cached phrases ({len(hashes)} files):")
                            for h in hashes:
                                print(f"  {h}")

                else:
                    print(f"Unknown command: {cmd}")
                    print("Type /help for available commands.")

            # Speak text
            else:
                if not current_user:
                    print("No user selected. Use /add or /user first.")
                    continue

                user_id = config["current_user"]

                # Check cache first
                cached_audio = get_cached_audio(user_id, text)
                if cached_audio:
                    print("(cached)")
                    player.play(cached_audio)
                else:
                    print("Generating speech...")
                    try:
                        audio = tts_client.text_to_speech(
                            text, current_user["voice_id"]
                        )
                        save_to_cache(user_id, text, audio)
                        player.play(audio)
                    except Exception as e:
                        print(f"Error: {e}")

    finally:
        player.cleanup()

    print("Goodbye!")


if __name__ == "__main__":
    main()
