import pyttsx3

class AudioManager:
    """Class to manage Text-to-Speech (TTS) functionalities."""

    def __init__(self):
        """Initialize the TTS engine."""
        self.engine = pyttsx3.init()  # Initialize the TTS engine
        self.set_properties()  # Set default properties for speech

    def set_properties(self, rate=150, volume=1.0):
        """Set properties for the TTS engine.

        Args:
            rate (int): Speed of speech (default is 150).
            volume (float): Volume level (0.0 to 1.0, default is 1.0).
        """
        self.engine.setProperty('rate', rate)  # Set speech rate
        self.engine.setProperty('volume', volume)  # Set volume level

    def speak(self, text, callback=None):
        """Convert text to speech and play it.

        Args:
            text (str): The text to be spoken.
            callback (function): Function to call when speech is done.
        """
        self.engine.say(text)  # Queue the text for speaking
        # Wait for the speech to finish and then call the callback
        self.engine.connect('finished-utterance', lambda name, completed: callback() if completed and callback else None)
        self.engine.runAndWait()  # Block while processing all queued commands

    def cleanup(self):
        """Cleanup resources (not strictly necessary with pyttsx3)."""
        self.engine.stop()  # Stop the TTS engine
