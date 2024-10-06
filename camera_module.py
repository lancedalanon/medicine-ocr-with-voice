from kivy.uix.camera import Camera
from kivy.uix.popup import Popup
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label

class CameraPopup(Popup):
    """Class to handle camera functionality in a popup"""

    def __init__(self, on_capture=None, **kwargs):
        """Initialize the CameraPopup with an optional capture callback."""
        super().__init__(**kwargs)  # Initialize the Popup
        self.on_capture = on_capture  # Callback for capture functionality

        # Create a Camera widget with a larger resolution
        self.camera = Camera(play=True, resolution=(1280, 720))  # Increased resolution for better quality

        # Create a main layout for the camera popup
        camera_layout = GridLayout(cols=1, size_hint=(1, 1), padding=10, spacing=10)
        camera_layout.add_widget(self.camera)

        # Create a label to indicate camera functionality (optional)
        label = Label(text="Capture the image or close the camera.", size_hint_y=None, height=40)
        camera_layout.add_widget(label)

        # Create a layout for the buttons, placing them side by side
        button_layout = GridLayout(cols=2, size_hint_y=None, height=40)  # Height is kept small for the buttons

        # Create a button to capture the image
        capture_button = Button(text="Capture", size_hint=(1, None), size_hint_y=1)  # Occupy full width, small height
        capture_button.bind(on_press=self.capture_image)  # Bind capture functionality
        button_layout.add_widget(capture_button)

        # Create a button to close the popup
        close_button = Button(text="Close", size_hint=(1, None), size_hint_y=1)  # Occupy full width, small height
        close_button.bind(on_press=self.close_popup)  # Bind close functionality
        button_layout.add_widget(close_button)

        # Add the button layout to the main camera layout
        camera_layout.add_widget(button_layout)

        # Set the popup content
        self.content = camera_layout
        self.size_hint = (0.9, 0.9)  # Set the size hint of the popup
        self.title = "Capture Image"  # Set a title for the popup

    def capture_image(self, instance):
        """Handle image capture."""
        if self.on_capture:
            self.on_capture(self.camera)  # Call the capture callback if provided

    def close_popup(self, instance):
        """Stop the camera and close the popup."""
        self.camera.play = False  # Stop the camera
        self.dismiss()  # Close the popup
