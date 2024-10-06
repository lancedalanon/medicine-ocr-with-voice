import pyttsx3
import pygame
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
import os
import time 

class TTSApp(App):
    """Main App class for the layout of the application"""
    
    def __init__(self, **kwargs):
        """Initialize the application and the text-to-speech engine"""
        super().__init__(**kwargs)
        self.tts_engine = pyttsx3.init()  # Initialize the TTS engine
        pygame.init()  # Initialize pygame for sound control
        self.is_speaking = False  # Track if TTS is currently speaking
        self.temp_file_path = "temp.wav"  # Static path for the temporary file

    def build(self):
        """Build the UI layout of the application"""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create a larger text input field for user input with transparent background
        self.text_input = TextInput(
            hint_text='Enter text here...',
            size_hint=(1, 0.7),  # Set height to 70%
            multiline=True,  # Enable multiline for wrapping
            background_color=(1, 1, 1, 0),  # Fully transparent
            foreground_color=(1, 1, 1, 1),  # Text color (white)
            font_size='32sp',  # Adjusted font size to 32
        )
        self.text_input.bind(text=self.on_text)  # Bind the text input to check for length
        layout.add_widget(self.text_input)

        # Button layout using GridLayout for two rows, set height to 30%
        button_layout = GridLayout(cols=2, size_hint=(1, 0.3), spacing=10)

        # TTS button
        self.tts_button = Button(text="Start", size_hint=(1, 1), font_size='20sp')  # Increase button size
        self.tts_button.bind(on_press=self.read)  # Bind the read method
        button_layout.add_widget(self.tts_button)

        # Stop button
        stop_button = Button(text="Stop", size_hint=(1, 1), font_size='20sp')  # Increase button size
        stop_button.bind(on_press=self.stop)  # Bind the stop method
        button_layout.add_widget(stop_button)

        # Capture button
        capture_button = Button(text="Capture", size_hint=(1, 1), font_size='20sp')  # Increase button size
        capture_button.bind(on_press=self.capture)  # Bind the capture method
        button_layout.add_widget(capture_button)

        # Quit button
        quit_button = Button(text="Quit", size_hint=(1, 1), font_size='20sp')  # Increase button size
        quit_button.bind(on_press=self.stop_app)  # Bind the quit method
        button_layout.add_widget(quit_button)

        layout.add_widget(button_layout)

        return layout

    def on_text(self, instance, value):
        """Limit the length of the input text to 5000 characters"""
        if len(value) > 5000:
            instance.text = value[:5000]  # Trim text to 5000 characters

    def read(self, instance):
        """Convert input text to speech and play it using pygame from a static file."""
        text = self.text_input.text.strip()  # Get trimmed text from input

        if text:
            self.is_speaking = True  # Mark that we are speaking

            # Check if temp.wav already exists and delete it
            if os.path.exists(self.temp_file_path):
                try:
                    pygame.mixer.music.stop()  # Stop any ongoing playback
                    pygame.mixer.music.unload()  # Unload the current music
                    os.remove(self.temp_file_path)  # Remove the old file
                except Exception as e:
                    print("Error removing old audio file:", e)  # Log any errors

            # Save TTS to the static temp.wav file
            self.tts_engine.save_to_file(text, self.temp_file_path)  # Save TTS to temp.wav
            self.tts_engine.runAndWait()  # Wait until the file is saved

            # Introduce a brief delay to ensure the file is fully written
            time.sleep(0.1)  # Sleep for 100 ms

            # Stop the mixer before re-initializing
            pygame.mixer.quit()  # Quit the mixer
            pygame.mixer.init()  # Re-initialize the mixer

            # Load and play the audio from the static file
            try:
                pygame.mixer.music.load(self.temp_file_path)  # Load the audio file
                pygame.mixer.music.play()  # Play the audio
                print("Playing audio from:", self.temp_file_path)  # Log the playback
            except Exception as e:
                print("Error loading or playing audio:", e)  # Log any errors

            # Schedule a check to update the status label after speaking
            Clock.schedule_once(self.check_playing, 0.1)  # Check playback status

    def check_playing(self, dt):
        """Check if the music is still playing and update the status label accordingly"""
        if not pygame.mixer.music.get_busy():
            self.is_speaking = False

    def stop(self, instance):
        """Stop the audio playback"""
        if self.is_speaking:
            pygame.mixer.music.stop()
            self.is_speaking = False

    def capture(self, instance):
        """Handle capture button press (custom functionality can be implemented here)"""
        pass  # You can implement capture functionality here

    def stop_app(self, instance):
        """Quit the application gracefully"""
        self.stop(instance)  # Stop any speaking
        App.get_running_app().stop()  # Stop the app

# Run the app
if __name__ == '__main__':
    TTSApp().run()
