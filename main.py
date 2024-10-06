from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from audio_manager import AudioManager  # Import the AudioManager
from camera_module import CameraPopup  # Import the CameraPopup class

class TTSApp(App):
    """Main App class for the Text-to-Speech mobile app"""

    def __init__(self, **kwargs):
        """Initialize the app and the AudioManager instance."""
        super().__init__(**kwargs)
        self.audio_manager = AudioManager()  # Initialize AudioManager

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

        # Capture button
        capture_button = Button(text="Capture")
        capture_button.bind(on_press=self.open_camera)
        button_layout.add_widget(capture_button)

        layout.add_widget(button_layout)

        # Status label
        self.status_label = Label(text="Click the button to hear the text", size_hint=(1, 0.1))
        layout.add_widget(self.status_label)

        return layout

    def text_to_speech(self, instance):
        """Convert the text input to speech and play it directly in the app"""
        text = self.text_input.text.strip()

        if not text:
            self.status_label.text = "Please enter some text!"
            return

        try:
            self.audio_manager.speak(text)
            self.status_label.text = "Playing speech..."
        except Exception as e:
            self.status_label.text = f"Error: {str(e)}"
            print(f"An error occurred: {e}")

    def open_camera(self, instance):
        """Open the camera using the CameraPopup module"""
        camera_popup = CameraPopup(on_capture=self.handle_capture)  # Pass capture callback
        camera_popup.open()

    def handle_capture(self, camera):
        """Handle the image capture from the camera"""
        # You can implement your logic for capturing the image here
        print("Capture image logic goes here!")

# Run the app
if __name__ == '__main__':
    TTSApp().run()
