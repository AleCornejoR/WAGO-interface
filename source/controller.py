# source.controller.py
from datetime import datetime
from time import sleep


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Conectar los botones a los métodos del controlador
        self.view.test_button.clicked.connect(self.handle_test_button_click)
        self.view.connect_button.clicked.connect(self.handle_connect_button_click)
        self.view.poweroff_button.clicked.connect(self.handle_poweroff_button_click)

        self.all_buttons = [
            self.view.connect_button,
            self.view.poweroff_button,
            self.view.test_button,
        ]

        self.initUI()

    def initUI(self):
        # Conectar señales de cambio de texto de los campos de entrada al método de validación
        for delay_name in self.view.config.get("delays", {}).keys():
            input_field = getattr(self.view, f"{delay_name}_input")
            input_field.textChanged.connect(self.validate_inputs)

        self.view.repetition_input.textChanged.connect(self.validate_inputs)

    def handle_test_button_click(self):
        # Aquí es donde manejarás la lógica cuando se presione el botón "Test"
        print("Test button clicked!")
        self.tester_log_message("[*] Initiating Test")

        # Obtener los valores del layout de tester
        repetitions = int(self.view.get_tester_value("repetition_num"))
        pre_solution_delay = float(self.view.get_tester_value("pre_solution"))
        solution_delay = float(self.view.get_tester_value("solution"))
        pos_solution_delay = float(self.view.get_tester_value("pos_solution"))
        between_rep_delay = float(self.view.get_tester_value("between_repetition"))

        # Definir las válvulas
        air_valve = self.view.get_tester_value("air_valve")
        solution_valve = self.view.get_tester_value("solution_valve")

        # Ejecutar la secuencia de acciones
        for _ in range(repetitions):
            self.model.toggleValve(air_valve)
            sleep(pre_solution_delay)

            self.model.toggleValve(solution_valve)
            sleep(solution_delay)
            self.model.toggleValve(solution_valve)
            sleep(pos_solution_delay)

            self.model.toggleValve(air_valve)
            sleep(between_rep_delay)

        self.tester_log_message("[+] Test completed without error\n")

    def handle_connect_button_click(self):
        # Aquí es donde manejarás la lógica cuando se presione el botón "Test"
        self.disable_buttons(self.all_buttons)
        print("Connect button clicked!")
        self.home_log_message(f"[*] Trying to connect to WAGO at IP {self.model.ip}...")

        self.model.connection()
        if self.model.connection_status == "FAIL":
            self.home_log_message(
                f"[!] Could not connect to WAGO at IP {self.model.ip}! Double-check IP address and connections.\n"
            )
        elif self.model.connection_status == "SUCCESS":
            self.home_log_message(f"[+] WAGO connected.")
            self.enable_buttons(self.all_buttons)

            self.home_log_message("[*] Setting valves.")
            self.model.resetValves()
            self.home_log_message("[+] Valves set.\n")

        self.view.connect_button.setEnabled(True)

    def handle_poweroff_button_click(self):
        # Aquí es donde manejarás la lógica cuando se presione el botón "Test"
        print("Poweroff button clicked!")
        self.home_log_message("[*] Shutting down valves")
        self.model.resetValvesN()
        self.home_log_message("[+] Valves Off\n")

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

    def disable_buttons(self, buttons):
        # Iterar sobre la lista de botones y desactivarlos
        for button in buttons:
            button.setEnabled(False)

    def enable_buttons(self, buttons):
        # Iterar sobre la lista de botones y desactivarlos
        for button in buttons:
            button.setEnabled(True)

    def validate_inputs(self):
        # Verificar si todos los campos de entrada tienen texto válido
        all_filled = True

        # Verificar campos de delay
        for delay_name in self.view.config.get("delays", {}).keys():
            input_field = getattr(self.view, f"{delay_name}_input")
            value = input_field.text().strip()
            if (
                not value or float(value) <= 0
            ):  # Comprobar si el campo está vacío o el valor es menor o igual a 0
                all_filled = False
                break

        # Verificar campo de repetición
        repetition_value = self.view.repetition_input.text().strip()
        if (
            not repetition_value or int(repetition_value) <= 0
        ):  # Comprobar si el campo está vacío o el valor es menor o igual a 0
            all_filled = False

        # Habilitar o deshabilitar el botón "Test" basado en si todos los campos están llenos y son mayores que 0
        self.view.test_button.setEnabled(all_filled)
