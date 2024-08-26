# main.py
import sys
import json
from PyQt6.QtWidgets import QApplication
from source.model import Model
from source.view import View
from source.controller import Controller


def load_config():
    try:
        with open("data/gui_config.json", "r") as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print("Configuration file not found. Using default settings.")
        return None
    except json.JSONDecodeError:
        print("Error decoding the JSON configuration file.")
        return None


def main():
    app = QApplication(sys.argv)
    # Cargar la configuración
    config = load_config()

    model = Model()
    view = View(config)
    controller = Controller(model, view)

    view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
