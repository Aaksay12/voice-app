"""Eleven Labs API client for text-to-speech."""

from elevenlabs import ElevenLabs


class TTSClient:
    """Wrapper around Eleven Labs API for text-to-speech."""

    def __init__(self, api_key: str):
        self.client = ElevenLabs(api_key=api_key)

    def text_to_speech(self, text: str, voice_id: str) -> bytes:
        """Convert text to speech and return mp3 audio bytes."""
        audio_generator = self.client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id="eleven_multilingual_v2",
            output_format="mp3_44100_128",
        )
        # Collect all chunks from the generator
        audio_bytes = b"".join(audio_generator)
        return audio_bytes
