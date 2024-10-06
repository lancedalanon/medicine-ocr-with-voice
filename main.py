import os
import time
import pyttsx3
import pygame
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.uix.popup import Popup
from kivy.uix.camera import Camera
from kivy.uix.image import Image
from kivy.graphics.texture import Texture
from PIL import Image as PILImage
import numpy as np
import easyocr

class TTSApp(App):
    """Main App class for the layout of the application."""

    def __init__(self, **kwargs):
        """Initialize the application and the text-to-speech engine."""
        super().__init__(**kwargs)
        self.tts_engine = pyttsx3.init()  # Initialize the TTS engine
        pygame.init()  # Initialize pygame for sound control
        self.is_speaking = False  # Track if TTS is currently speaking
        self.is_paused = False  # Track if TTS is currently paused
        self.temp_file_path = "temp.wav"  # Path for the temporary audio file
        self.camera = None  # Camera instance
        self.reader = easyocr.Reader(['en'])  # Initialize EasyOCR reader

    def build(self):
        """Build the UI layout of the application."""
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Create a larger text input field for user input
        self.text_input = TextInput(
            hint_text='Enter text here...',
            size_hint=(1, 0.7),  # Height set to 70%
            multiline=True,  # Enable multiline for wrapping
            background_color=(1, 1, 1, 0),  # Fully transparent
            foreground_color=(1, 1, 1, 1),  # Text color (white)
            font_size='32sp',  # Adjusted font size
        )
        self.text_input.bind(text=self.on_text)  # Limit text length
        layout.add_widget(self.text_input)

        # Button layout using GridLayout
        button_layout = self.create_button_layout()
        layout.add_widget(button_layout)

        return layout

    def create_button_layout(self):
        """Create and return the layout for buttons."""
        button_layout = GridLayout(cols=2, size_hint=(1, 0.3), spacing=10)

        # TTS Button
        self.tts_button = Button(text="Start", size_hint=(1, 1), font_size='20sp')
        self.tts_button.bind(on_press=self.toggle_read)
        button_layout.add_widget(self.tts_button)

        # Pause/Unpause Button
        self.pause_button = Button(text="Pause", size_hint=(1, 1), font_size='20sp')
        self.pause_button.bind(on_press=self.toggle_pause)
        button_layout.add_widget(self.pause_button)

        # Capture Button
        capture_button = Button(text="Capture", size_hint=(1, 1), font_size='20sp')
        capture_button.bind(on_press=self.show_camera_popup)  # Open camera popup
        button_layout.add_widget(capture_button)

        # Quit Button
        quit_button = Button(text="Quit", size_hint=(1, 1), font_size='20sp')
        quit_button.bind(on_press=self.stop_app)
        button_layout.add_widget(quit_button)

        return button_layout

    def on_text(self, instance, value):
        """Limit the length of the input text to 5000 characters."""
        instance.text = value[:5000]  # Trim text to 5000 characters

    def toggle_read(self, instance):
        """Toggle between reading text and stopping playback."""
        if not self.is_speaking:
            self.read(instance)  # Start reading
            self.tts_button.text = "Stop"  # Change button text to "Stop"
        else:
            self.stop(instance)  # Stop reading
            self.tts_button.text = "Start"  # Change button text back to "Start"

    def read(self, instance):
        """Convert input text to speech and play it using pygame."""
        text = self.text_input.text.strip()
        print(text)

        if text and not self.is_speaking:
            self.is_speaking = True
            self.prepare_audio_file(text)  # Prepare audio file

            # Load and play the audio from the temporary file
            self.play_audio()

            # Schedule a check to update the speaking status
            Clock.schedule_once(self.check_playing, 0.1)

    def prepare_audio_file(self, text):
        """Prepare the audio file for TTS output."""
        # Stop any currently playing music before removing the old audio file
        pygame.mixer.music.stop()

        # Unload any previously loaded music before loading a new file
        pygame.mixer.music.unload()

        # Remove old audio file if it exists
        if os.path.exists(self.temp_file_path):
            try:
                os.remove(self.temp_file_path)
            except Exception as e:
                print("Error removing old audio file:", e)

        # Save TTS to the temporary file
        self.tts_engine.save_to_file(text, self.temp_file_path)
        self.tts_engine.runAndWait()
        time.sleep(0.1)  # Brief delay to ensure the file is written

    def play_audio(self):
        """Load and play the audio from the temporary file."""
        pygame.mixer.quit()  # Ensure no old mixer is running
        pygame.mixer.init()  # Initialize the mixer

        try:
            pygame.mixer.music.load(self.temp_file_path)  # Load the new audio file
            pygame.mixer.music.play()  # Play the audio
            print("Playing audio from:", self.temp_file_path)
        except Exception as e:
            print("Error loading or playing audio:", e)

    def check_playing(self, dt):
        """Check if the music is still playing and update the status."""
        if not pygame.mixer.music.get_busy():
            self.is_speaking = False
            self.tts_button.text = "Start"  # Reset button text after speaking

    def stop(self, instance):
        """Stop the audio playback."""
        if self.is_speaking:
            pygame.mixer.music.stop()  # Stop the music before changing state
            self.is_speaking = False
            self.tts_button.text = "Start"  # Reset button text

    def toggle_pause(self, instance):
        """Toggle between pausing and unpausing the audio playback."""
        if self.is_paused:
            pygame.mixer.music.unpause()  # Unpause the audio
            self.pause_button.text = "Pause"  # Change button text to "Pause"
            self.is_paused = False
        else:
            pygame.mixer.music.pause()  # Pause the audio
            self.pause_button.text = "Unpause"  # Change button text to "Unpause"
            self.is_paused = True

    def stop_app(self, instance):
        """Stop the application."""
        self.stop(instance)
        quit()

    def show_camera_popup(self, instance):
        """Show a popup with the camera for capturing images."""
        camera_popup = Popup(title="Capture Image", size_hint=(0.8, 0.8))
        camera_layout = BoxLayout(orientation='vertical')

        try:
            # Initialize the camera
            self.camera = Camera(play=True, resolution=(1280, 720))  # Set higher resolution
            if not self.camera:  # Check if the camera was initialized successfully
                raise Exception("Camera not initialized properly.")
            camera_layout.add_widget(self.camera)
        except Exception as e:
            print("Failed to initialize camera:", e)
            self.show_popup("Could not access the camera.")  # Notify user
            return

        # Add buttons to capture and close
        capture_button = Button(text="Capture", size_hint=(1, 0.1))
        capture_button.bind(on_press=self.capture_image)
        camera_layout.add_widget(capture_button)

        close_button = Button(text="Close", size_hint=(1, 0.1))
        close_button.bind(on_press=camera_popup.dismiss)  # Close the popup
        camera_layout.add_widget(close_button)

        camera_popup.content = camera_layout
        camera_popup.open()  # Open the camera popup

    def capture_image(self, instance):
        """Capture an image from the camera and process it."""
        if self.camera:
            # Convert the camera image to a numpy array
            texture = self.camera.texture
            if texture:
                # Convert Kivy texture to a PIL Image
                image_data = texture.pixels
                width, height = texture.size
                image = PILImage.frombytes('RGBA', (width, height), image_data)

                # Flip the image vertically
                image = image.transpose(PILImage.FLIP_TOP_BOTTOM)

                # Convert to RGB
                image = image.convert('RGB')
                image_np = np.array(image)

                # Use EasyOCR to read text from the image
                result = self.reader.readtext(image_np)
                text = " ".join([res[1] for res in result])

                if text:
                    self.text_input.text = text  # Display recognized text in TextInput
                    self.show_image_popup(image)  # Show captured image in a popup
                    self.read(text)  # Automatically read the recognized text
            else:
                print("Failed to get texture from camera.")

    def show_image_popup(self, image):
        """Show a popup to display the captured image."""
        image_popup = Popup(title="Captured Image", size_hint=(0.8, 0.8))
        image_widget = Image(size_hint=(1, 1))

        # Convert PIL image to Kivy texture
        image_texture = self.pil_to_texture(image)
        image_widget.texture = image_texture
        image_popup.content = image_widget
        image_popup.open()

    def pil_to_texture(self, pil_image):
        """Convert a PIL Image to a Kivy texture."""
        pil_image = pil_image.convert('RGBA')
        texture = Texture.create(size=pil_image.size)
        texture.blit_buffer(pil_image.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
        return texture

if __name__ == '__main__':
    TTSApp().run()
