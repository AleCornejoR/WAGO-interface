# main.py

# Standard library imports
import json
import sys

# Third-party imports
from PyQt6.QtWidgets import QApplication

# Local application imports
from source.controller import Controller
from source.model import WagoPLC
from source.view import View


def load_config(filepath="data/gui_config.json"):
    """
    Loads a JSON configuration file.

    This function attempts to load the configuration from a specified JSON file.
    If the file is not found or cannot be decoded, it will return None and print an error message.

    Parameters:
    - filepath (str): The path to the configuration file. Defaults to "data/gui_config.json".

    Returns:
    - dict: The loaded configuration as a dictionary if successful.
    - None: If the file is not found or if there is a decoding error.
    """
    try:
        with open(filepath, "r") as config_file:
            return json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading configuration: {e}")
        return None


def load_settings(filepath="data/settings.json"):
    """
    Loads the settings from a JSON file.

    This function attempts to load settings from a specified JSON file. If the file is not found
    or cannot be decoded, it returns default settings and prints an error message.

    Parameters:
    - filepath (str): The path to the settings file. Defaults to "data/settings.json".

    Returns:
    - dict: The loaded settings as a dictionary if successful.
    - dict: Default settings if the file is not found or if there is a decoding error.
    """
    default_settings = {
        "ip": "192.168.1.8",
        "coils": 16,
        "actLow": True,
        "virtual": False,
    }

    try:
        with open(filepath, "r") as settings_file:
            return json.load(settings_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading settings: {e}. Using default settings.")
        return default_settings


def main():
    """
    Entry point for the application.

    This function initializes the application, loads configuration and settings,
    and sets up the MVC (Model-View-Controller) architecture. It then starts the
    main event loop of the application.
    """
    app = QApplication(sys.argv)

    # Load configuration and settings
    config = load_config()
    settings = load_settings()

    # Extract individual parameters from settings
    ip = settings.get("ip", "192.168.1.8")
    coils = settings.get("coils", 16)
    actLow = settings.get("actLow", True)
    virtual = settings.get("virtual", False)

    # Initialize the model, view, and controller
    model = WagoPLC(ip, coils, actLow, virtual=virtual)
    view = View(config)
    controller = Controller(model, view)

    # Display the main window
    view.show()

    # Start the application's event loop
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
