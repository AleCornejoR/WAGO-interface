# source.controller.py
from datetime import datetime


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Conectar los botones a los métodos del controlador
        self.view.test_button.clicked.connect(self.handle_test_button_click)
        self.view.connect_button.clicked.connect(self.handle_connect_button_click)
        self.view.poweroff_button.clicked.connect(self.handle_poweroff_button_click)

    def handle_test_button_click(self):
        # Aquí es donde manejarás la lógica cuando se presione el botón "Test"
        print("Test button clicked!")

        self.tester_log_message("[*] Test button clicked!")

    def handle_connect_button_click(self):
        # Aquí es donde manejarás la lógica cuando se presione el botón "Test"
        print("Connect button clicked!")

        self.home_log_message("[*] Connect button clicked!")

    def handle_poweroff_button_click(self):
        # Aquí es donde manejarás la lógica cuando se presione el botón "Test"
        print("Poweroff button clicked!")

        self.home_log_message("[*] Poweroff button clicked!")

    def home_log_message(self, message):
        # Obtener la hora actual en formato HH:MM:SS
        timestamp = datetime.now().strftime("[%H:%M:%S]")

        # Concatenar el timestamp con el mensaje
        full_message = f"{timestamp} {message}"

        # Obtener el texto actual del log box
        current_text = self.view.home_log_box.toPlainText()

        # Concatenar el nuevo mensaje al texto existente
        new_text = current_text + "\n" + full_message

        # Establecer el texto actualizado en el log box
        self.view.home_log_box.setPlainText(new_text)

        # Desplazar la vista hacia el final del log box
        scrollbar = self.view.home_log_box.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def tester_log_message(self, message):
        # Obtener la hora actual en formato HH:MM:SS
        timestamp = datetime.now().strftime("[%H:%M:%S]")

        # Concatenar el timestamp con el mensaje
        full_message = f"{timestamp} {message}"

        # Obtener el texto actual del log box
        current_text = self.view.tester_log_box.toPlainText()

        # Concatenar el nuevo mensaje al texto existente
        new_text = current_text + "\n" + full_message

        # Establecer el texto actualizado en el log box
        self.view.tester_log_box.setPlainText(new_text)

        # Desplazar la vista hacia el final del log box
        scrollbar = self.view.tester_log_box.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
