# main.py
import sys
import json
from PyQt6.QtWidgets import QApplication
from source.model import WagoPLC
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


def load_settings():
    try:
        with open("data/settings.json", "r") as settings_file:
            settings = json.load(settings_file)
            return settings
    except FileNotFoundError:
        print("Settings file not found. Using default settings.")
        return {"ip": "192.168.1.8", "coils": 16, "actLow": True, "virtual": False}
    except json.JSONDecodeError:
        print("Error decoding the JSON settings file.")
        return {"ip": "192.168.1.8", "coils": 16, "actLow": True, "virtual": False}


def main():
    app = QApplication(sys.argv)

    # Cargar la configuración
    config = load_config()

    # Cargar la configuración del archivo settings.json
    settings = load_settings()

    # Extraer parámetros individuales del diccionario settings
    ip = settings.get("ip", "192.168.1.8")
    coils = settings.get("coils", 16)
    actLow = settings.get("actLow", True)
    virtual = settings.get("virtual", False)

    # Pasar los parámetros extraídos a WagoPLC
    model = WagoPLC(ip, coils, actLow, virtual=virtual)
    view = View(config)
    controller = Controller(model, view)

    view.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
