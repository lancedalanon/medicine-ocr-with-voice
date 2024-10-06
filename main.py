from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock  # Import Clock for scheduling tasks
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


class TTSApp(App):
    """Main App class for the Text-to-Speech mobile app"""

    def __init__(self, **kwargs):
        """Initialize the app and the AudioManager instance."""
        super().__init__(**kwargs)
        self.audio_manager = AudioManager()  # Initialize AudioManager
        self.original_text = ""  # Store the original text for resetting

    def build(self):
        """Build the UI and logic of the application"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create a larger text input field for user input
        self.text_input = TextInput(
            hint_text='Enter text here...',
            size_hint=(1, 0.8),
            multiline=False,
            background_color=(1, 1, 1, 0),
            foreground_color=(1, 1, 1, 1),
            font_size='32sp',
            background_normal='',
            background_active=''
        )
        layout.add_widget(self.text_input)

        # Button layout
        button_layout = BoxLayout(size_hint=(1, 0.1), spacing=10)

        # TTS button
        tts_button = Button(text="Speak")
        tts_button.bind(on_press=self.text_to_speech)
        button_layout.add_widget(tts_button)

        # Capture button (updated to print a message)
        capture_button = Button(text="Capture")
        capture_button.bind(on_press=self.capture_action)
        button_layout.add_widget(capture_button)

        layout.add_widget(button_layout)

        # Status label
        self.status_label = Label(text="Click the button to hear the text", size_hint=(1, 0.1))
        layout.add_widget(self.status_label)

        return layout

    def text_to_speech(self, instance):
        """Convert the text input to speech and play it directly in the app"""
        text = self.text_input.text.strip()
        self.status_label.text = "Playing speech..."  # Update status label

        if not text:
            self.status_label.text = "Please enter some text!"
            return

        # Store the original text to reset later
        self.original_text = text

        # Schedule the TTS action to ensure the label updates immediately
        Clock.schedule_once(lambda dt: self._perform_speech(text), 0)

    def _perform_speech(self, text):
        """Perform the actual text-to-speech action."""
        try:
            # Pass a callback to reset the text field when speaking is done
            self.audio_manager.speak(text, self.reset_text_input)
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"
            print(f"An error occurred: {e}")

    def reset_text_input(self):
        """Reset the text input field to its original text."""
        self.text_input.text = self.original_text  # Restore the original text
        self.status_label.text = "Click the button to hear the text"  # Reset status message

    def capture_action(self, instance):
        """Handle capture action by printing a message"""
        print("Capture button pressed!")

# Run the app
if __name__ == '__main__':
    TTSApp().run()
