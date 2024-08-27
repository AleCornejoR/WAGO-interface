# source.controller.py
from datetime import datetime
from time import sleep


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view

        # Connect the view's buttons to their corresponding controller methods
        self._connect_signals()

        # Gather all buttons into a list for easier management
        self.all_buttons = self._gather_buttons()
        self.home_log = self.view.home_log_box
        self.tester_log = self.view.tester_log_box

        # Initialize the user interface
        self.initUI()

    def _connect_signals(self):
        """Connect the view's buttons to their corresponding controller methods."""
        self.view.test_button.clicked.connect(self.handle_test_button_click)
        self.view.connect_button.clicked.connect(self.handle_connect_button_click)
        self.view.poweroff_button.clicked.connect(self.handle_poweroff_button_click)

    def _gather_buttons(self):
        """Collect all buttons from the view into a list."""
        return [
            self.view.connect_button,
            self.view.poweroff_button,
            self.view.test_button,
        ]

    def initUI(self):
        """
        Initialize the user interface by connecting input field signals to validation methods.
        """
        # Connect text change signals for delay input fields to the validation method
        self._connect_delay_inputs()

        # Connect the text change signal for the repetition input field to the validation method
        self.view.repetition_input.textChanged.connect(self.validate_inputs)

    def _connect_delay_inputs(self):
        """
        Connect the text change signals of delay input fields to the validation method.
        """
        for delay_name in self.view.config.get("delays", {}).keys():
            input_field = getattr(self.view, f"{delay_name}_input")
            input_field.textChanged.connect(self.validate_inputs)

    def handle_test_button_click(self):
        """
        Handle the logic when the 'Test' button is clicked.
        """
        # Log the initiation of the test
        print("Test button clicked!")
        self.model.connection()
        self._handle_connection_status()
        self._log_message("[*] Initiating Test", self.tester_log)

        # Retrieve values from the tester layout
        repetitions = int(self.view.get_tester_value("repetition_num"))
        delays = {
            "pre_solution": float(self.view.get_tester_value("pre_solution")),
            "solution": float(self.view.get_tester_value("solution")),
            "pos_solution": float(self.view.get_tester_value("pos_solution")),
            "between_rep": float(self.view.get_tester_value("between_repetition")),
        }

        # Define the valves
        air_valve = int(self.view.get_tester_value("air_valve")) - 1
        solution_valve = int(self.view.get_tester_value("solution_valve")) - 1

        # Execute the sequence of actions
        for _ in range(repetitions):
            self._perform_test_cycle(air_valve, solution_valve, delays)

        self._log_message("[+] Test completed without error\n", self.tester_log)

    def _perform_test_cycle(self, air_valve, solution_valve, delays):
        """
        Perform a single test cycle based on the provided valve settings and delays.

        Parameters:
        - air_valve (str): The identifier for the air valve.
        - solution_valve (str): The identifier for the solution valve.
        - delays (dict): A dictionary containing delay times for each step.
        """
        self.model.toggleValve(air_valve)
        sleep(delays["pre_solution"])

        self.model.toggleValve(solution_valve)
        sleep(delays["solution"])
        self.model.toggleValve(solution_valve)
        sleep(delays["pos_solution"])

        self.model.toggleValve(air_valve)
        sleep(delays["between_rep"])

    def handle_connect_button_click(self):
        """
        Handle the logic when the 'Connect' button is clicked.
        """
        # Disable all buttons during connection attempt
        self.set_buttons(self.all_buttons, False)
        print("Connect button clicked!")
        self._log_message(
            f"[*] Trying to connect to WAGO at IP {self.model.ip}...",
            self.home_log,
        )

        # Attempt to establish a connection
        self.model.connection()
        self._handle_connection_status()

        # Re-enable the 'Connect' button
        self.view.connect_button.setEnabled(True)

    def _handle_connection_status(self):
        """
        Handle the outcome of the connection attempt based on the model's connection status.
        """
        if self.model.connection_status == "FAIL":
            self.set_buttons(self.all_buttons, False)
            self._log_message(
                f"[!] Could not connect to WAGO at IP {self.model.ip}! Double-check IP address and connections.\n",
                self.home_log,
            )
        elif self.model.connection_status == "SUCCESS":
            self._log_message(f"[+] WAGO connected.", self.home_log)
            self.set_buttons(self.all_buttons, True)

            self._initialize_valves()

    def _initialize_valves(self):
        """
        Reset and initialize the valves after a successful connection.
        """
        self.__log_message("[*] Setting valves.", self.home_log)
        self.model.resetValves()
        self.__log_message("[+] Valves set.\n", self.home_log)

    def handle_poweroff_button_click(self):
        """
        Handle the logic when the 'Poweroff' button is clicked.
        """
        print("Poweroff button clicked!")

        # Attempt to connect to the model
        self.model.connection()
        self._handle_connection_status()

        # Shut down the valves
        self._shutdown_valves()

    def _shutdown_valves(self):
        """
        Shut down the valves and log the operation.
        """
        self._log_message("[*] Shutting down valves", self.home_log)
        self.model.resetValvesN()
        self._log_message("[+] Valves Off\n", self.home_log)

    def _log_message(self, message, log_box):
        """
        Update the specified log box with a new message and scroll to the bottom.

        Parameters:
        - message (str): The message to add to the log box.
        - log_box (QPlainTextEdit): The log box widget to update.
        """
        # Get the current timestamp in HH:MM:SS format
        timestamp = datetime.now().strftime("[%H:%M:%S]")

        # Format the full message with the timestamp
        full_message = f"{timestamp} {message}"

        # Get the current text from the log box
        current_text = log_box.toPlainText()

        # Append the new message to the existing text
        new_text = f"{current_text}\n{full_message}"

        # Set the updated text in the log box
        log_box.setPlainText(new_text)

        # Scroll to the bottom of the log box
        scrollbar = log_box.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def set_buttons(self, buttons, state):
        """
        Enable or disable a list of buttons based on the 'state' parameter.

        Parameters:
        - buttons (list): A list of buttons to enable or disable.
        - state (bool): True to enable buttons, False to disable them.
        """
        for button in buttons:
            button.setEnabled(state)

    def validate_inputs(self):
        """
        Validate all input fields to ensure they are filled with valid values.
        """
        # Check if all delay input fields have valid values
        if not self._validate_delay_inputs():
            self.view.test_button.setEnabled(False)
            return

        # Check if the repetition input field has a valid value
        if not self._validate_repetition_input():
            self.view.test_button.setEnabled(False)
            return

        # Enable the 'Test' button if all inputs are valid
        self.view.test_button.setEnabled(True)

    def _validate_delay_inputs(self):
        """
        Validate delay input fields to ensure they have positive values.

        Returns:
        - bool: True if all delay inputs are valid, False otherwise.
        """
        for delay_name in self.view.config.get("delays", {}).keys():
            input_field = getattr(self.view, f"{delay_name}_input")
            value = input_field.text().strip()
            if not value or float(value) <= 0:
                return False
        return True

    def _validate_repetition_input(self):
        """
        Validate the repetition input field to ensure it has a positive value.

        Returns:
        - bool: True if the repetition input is valid, False otherwise.
        """
        repetition_value = self.view.repetition_input.text().strip()
        return bool(repetition_value) and int(repetition_value) > 0
