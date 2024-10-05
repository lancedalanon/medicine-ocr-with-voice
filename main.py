from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from audio_manager import AudioManager  # Import the AudioManager

class TTSApp(App):
    """Main App class for the Text-to-Speech mobile app"""

    def __init__(self, **kwargs):
        """Initialize the app and the AudioManager instance."""
        super().__init__(**kwargs)
        self.audio_manager = AudioManager()  # Initialize AudioManager

    def build(self):
        """Build the UI and logic of the application"""

        # Main layout to arrange widgets vertically
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create a larger text input field for user input
        self.text_input = TextInput(
            hint_text='Enter text here...',
            size_hint=(1, 0.8),  # Increase vertical space allocation
            multiline=False,
            background_color=(1, 1, 1, 0),  # Transparent background to blend with layout
            foreground_color=(1, 1, 1, 1),  # Text color (white)
            font_size='32sp',  # Increase font size
            background_normal='',  # Remove normal background image
            background_active=''  # Remove active background image
        )
        layout.add_widget(self.text_input)

        # Create a button for TTS functionality
        tts_button = Button(text="Speak", size_hint=(1, 0.1))
        tts_button.bind(on_press=self.text_to_speech)  # Bind button press to text-to-speech function
        layout.add_widget(tts_button)

        # Create a label to show the status
        self.status_label = Label(text="Click the button to hear the text", size_hint=(1, 0.1))
        layout.add_widget(self.status_label)

        return layout

    def text_to_speech(self, instance):
        """Convert the text input to speech and play it directly in the app"""

        # Get text input from the user
        text = self.text_input.text.strip()

        # Input validation: check if text is empty
        if not text:
            self.status_label.text = "Please enter some text!"
            return

        try:
            # Speak the text using the AudioManager
            self.audio_manager.speak(text)  # Use the AudioManager to speak the text

            # Update the status label
            self.status_label.text = "Playing speech..."

        except Exception as e:
            # Handle any errors that may occur during TTS generation or playback
            self.status_label.text = f"Error: {str(e)}"
            print(f"An error occurred: {e}")

# Run the app
if __name__ == '__main__':
    TTSApp().run()
