"""Audio player using pygame.mixer for mp3 playback."""

import io
import pygame


class AudioPlayer:
    """Play mp3 audio files using pygame.mixer."""

    def __init__(self):
        pygame.mixer.init()

    def play(self, audio_data: bytes) -> None:
        """Play mp3 audio data."""
        audio_file = io.BytesIO(audio_data)
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        # Wait for playback to finish
        while pygame.mixer.music.get_busy():
            pygame.time.wait(100)

    def stop(self) -> None:
        """Stop current playback."""
        pygame.mixer.music.stop()

    def cleanup(self) -> None:
        """Clean up pygame resources."""
        pygame.mixer.quit()
