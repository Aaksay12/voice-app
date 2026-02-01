# Eleven Labs Voice App

A CLI Python application for text-to-speech using the Eleven Labs API. Supports multiple users with different voices and caches audio for faster playback of repeated phrases.

## Features

- **Text-to-Speech**: Type any text to hear it spoken aloud
- **Multi-User Support**: Configure multiple users with different Eleven Labs voice IDs
- **Audio Caching**: Automatically caches generated audio to avoid redundant API calls
- **Simple CLI**: Easy-to-use command-line interface

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Aaksay12/voice-app.git
   cd voice-app
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up your configuration:
   ```bash
   cp users.json.template users.json
   ```

4. Set your Eleven Labs API key:
   ```bash
   export ELEVENLABS_API_KEY="your-api-key-here"
   ```

## Usage

Run the application:
```bash
python main.py
```

### Commands

| Command | Description |
|---------|-------------|
| `<text>` | Speak the entered text |
| `/user <id>` | Switch to a different user |
| `/users` | List all configured users |
| `/add <id> <voice_id> <name>` | Add a new user |
| `/cache <phrase>` | Pre-cache a phrase for instant playback |
| `/list-cache` | List cached phrases for current user |
| `/help` | Show help message |
| `/quit` | Exit the application |

### Example Session

```
$ python main.py
Eleven Labs Voice App
Type /help for commands, /quit to exit

No user configured. Use /add to create one.
> /add alice EXAVITQu4vr4xnSDxMaL Alice
Added user: Alice
> Hello, this is a test!
Generating speech...
> Hello, this is a test!
(cached)
> /cache Welcome to the voice app!
Caching phrase...
Phrase cached successfully.
> /quit
Goodbye!
```

## Configuration

The `users.json` file stores user configurations:

```json
{
  "users": {
    "alice": {
      "voice_id": "EXAVITQu4vr4xnSDxMaL",
      "name": "Alice"
    }
  },
  "current_user": "alice",
  "api_key": ""
}
```

- **voice_id**: Eleven Labs voice ID (find these in your Eleven Labs dashboard)
- **api_key**: Can be set here or via `ELEVENLABS_API_KEY` environment variable (recommended)

## Finding Voice IDs

1. Log in to [Eleven Labs](https://elevenlabs.io/)
2. Go to the Voices section
3. Click on a voice to view its details
4. Copy the Voice ID from the voice settings

## License

MIT
