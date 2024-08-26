# view.py
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QTabWidget,
    QFormLayout,
    QTextEdit,
)
from PyQt6.QtGui import QPixmap, QDoubleValidator, QIntValidator  # Import validators


class View(QWidget):
    def __init__(self, config=None):
        super().__init__()
        self.config = config
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.config["window"]["title"])

        # Set fixed size from config
        window_width = self.config["window"].get(
            "width", 800
        )  # Default to 800 if not specified
        window_height = self.config["window"].get(
            "height", 400
        )  # Default to 600 if not specified
        self.setFixedSize(window_width, window_height)

        # Create a tab widget
        self.tabs = QTabWidget()

        # Create and set up the Home tab
        self.home_tab = QWidget()
        self.setup_home_tab()
        self.tabs.addTab(self.home_tab, self.config["tabs"]["home_tab"]["name"])

        # Create the main tab
        self.tester_tab = QWidget()
        self.setup_tester_tab()
        self.tabs.addTab(self.tester_tab, self.config["tabs"]["tester_tab"]["name"])

        # Create the settings tab
        self.settings_tab = QWidget()
        # self.setup_main_tab()
        self.tabs.addTab(self.settings_tab, self.config["tabs"]["settings_tab"]["name"])

        # Main layout for the window
        window_layout = QVBoxLayout()
        window_layout.addWidget(self.tabs)
        self.setLayout(window_layout)

    def setup_home_tab(self):
        layout = QVBoxLayout()

        # Crear un layout horizontal para los botones
        button_layout = QHBoxLayout()

        # Botón de conexión
        self.connect_button = QPushButton(
            self.config["buttons"]["connect_button"]["label"]
        )
        self.apply_button_styles(
            self.connect_button, self.config["buttons"]["connect_button"]["style"]
        )
        button_layout.addWidget(self.connect_button)

        # Botón de apagado de válvulas
        self.poweroff_button = QPushButton(
            self.config["buttons"]["poweroff_button"]["label"]
        )
        self.apply_button_styles(
            self.poweroff_button, self.config["buttons"]["poweroff_button"]["style"]
        )
        button_layout.addWidget(self.poweroff_button)

        # Añadir el layout de botones al layout principal
        layout.addLayout(button_layout)

        # Cuadro de texto para logs
        self.home_log_box = QTextEdit()
        self.home_log_box.setPlaceholderText(
            self.config["log_box"]["home"]["placeholder"]
        )
        self.home_log_box.setReadOnly(
            True
        )  # Hacer que el cuadro de texto sea de solo lectura
        self.apply_text_box_styles(
            self.home_log_box, self.config["log_box"]["home"]["style"]
        )
        layout.addWidget(self.home_log_box)

        self.home_tab.setLayout(layout)

    def setup_tester_tab(self):
        # Main layout for the tab
        self.tester_layout = QHBoxLayout(self.tester_tab)

        # Layout for information input fields on the left
        self.form_layout = QFormLayout()

        self.solution_valve_combobox = QComboBox()
        self.gas_valve_combobox = QComboBox()

        # Set up dropdowns using the configuration
        self.setup_dropdowns()

        self.form_layout.addRow(
            QLabel(self.config["solution_valve"]["label"]), self.solution_valve_combobox
        )
        self.form_layout.addRow(
            QLabel(self.config["gas_valve"]["label"]), self.gas_valve_combobox
        )

        # Create input fields using configuration and validators
        self.create_input_fields()

        # Add the form layout to the left
        self.tester_layout.addLayout(self.form_layout)

        # Layout for the image and button on the right
        self.right_layout = QVBoxLayout()

        # Cuadro de texto para logs
        self.tester_log_box = QTextEdit()
        self.tester_log_box.setPlaceholderText(
            self.config["log_box"]["tester"]["placeholder"]
        )
        self.tester_log_box.setReadOnly(
            True
        )  # Hacer que el cuadro de texto sea de solo lectura
        self.apply_text_box_styles(
            self.tester_log_box, self.config["log_box"]["tester"]["style"]
        )
        self.right_layout.addWidget(self.tester_log_box)

        # "Test" button below the image
        self.test_button = QPushButton(self.config["buttons"]["test_button"]["label"])
        self.apply_button_styles(
            self.test_button, self.config["buttons"]["test_button"]["style"]
        )
        self.right_layout.addWidget(self.test_button)

        # Add the right layout to the main layout
        self.tester_layout.addLayout(self.right_layout)

    def setup_dropdowns(self):
        # Generate options for the dropdowns based on the number of valves
        num_valves = self.config.get("num_valves", 8)  # Default value is 8
        valve_options = [str(i) for i in range(num_valves)]

        # Configure the dropdowns
        self.solution_valve_combobox.addItems(valve_options)
        self.gas_valve_combobox.addItems(valve_options)

        # Get default values from the configuration
        default_solution_valve = self.config.get("solution_valve", {}).get(
            "default_value", "0"
        )
        default_gas_valve = self.config.get("gas_valve", {}).get("default_value", "0")

        # Set default values if they exist
        self.solution_valve_combobox.setCurrentText(default_solution_valve)
        self.gas_valve_combobox.setCurrentText(default_gas_valve)

    def create_input_fields(self):
        # Validators
        float_validator = QDoubleValidator()  # Validator for float numbers
        int_validator = QIntValidator()  # Validator for integer numbers

        # Configuration for delay fields
        delays_config = self.config.get("delays", {})
        for delay_name, delay_info in delays_config.items():
            input_field = QLineEdit()
            input_field.setText(
                delay_info.get("default_value", "")
            )  # Use the default value

            # Assign validator based on the type specified in the configuration
            if delay_info.get("type") == "float":
                input_field.setValidator(float_validator)
            elif delay_info.get("type") == "int":
                input_field.setValidator(int_validator)

            # Add the field to the form layout
            self.form_layout.addRow(QLabel(delay_info["label"]), input_field)

            # Save the reference of the input field for future use if necessary
            setattr(self, f"{delay_name}_input", input_field)

        # Repetition field
        repetition_config = self.config.get("repetition_num", {})
        repetition_input = QLineEdit()
        repetition_input.setText(repetition_config.get("default_value", ""))

        # Assign validator based on the type specified in the configuration
        if repetition_config.get("type") == "float":
            repetition_input.setValidator(float_validator)
        elif repetition_config.get("type") == "int":
            repetition_input.setValidator(int_validator)

        # Add the field to the form layout
        self.form_layout.addRow(QLabel(repetition_config["label"]), repetition_input)

        # Save the reference of the input field for future use if necessary
        setattr(self, "repetition_input", repetition_input)

    def apply_button_styles(self, button, style_config):
        padding = style_config["padding"]
        min_width = style_config["min-width"]
        max_width = style_config["max-width"]

        bg_color = style_config["background-color"]
        border_radius = style_config["border-radius"]
        text_color = style_config["color"]

        hover_bg_color = style_config["hover-background-color"]
        hover_text_color = style_config["hover-color"]

        pressed_bg_color = style_config["pressed-background-color"]
        pressed_text_color = style_config["pressed-color"]

        disabled_bg_color = style_config["disabled-background-color"]
        disabled_text_color = style_config["disabled-color"]

        # Crear la cadena de estilo CSS
        style_sheet = f"""
            QPushButton {{
                border-radius: {border_radius};  /* Establece las esquinas redondeadas */
                background-color: {bg_color};  /* Color de fondo */
                color: {text_color};  /* Color del texto */
                padding: {padding};  /* Relleno interno */
                min-width: {min_width};  /* Ancho mínimo del botón */
                max-width: {max_width};  /* Ancho máximo del botón */
            }}
            QPushButton:hover {{
                background-color: {hover_bg_color};  /* Color de fondo cuando se pasa el cursor sobre el botón */
                color: {hover_text_color};  /* Color del texto */
            }}
            QPushButton:pressed {{
                background-color: {pressed_bg_color};  /* Color de fondo cuando se pasa el cursor sobre el botón */
                color: {pressed_text_color};  /* Color del texto */
            }}
            QPushButton:disabled {{
                background-color: {disabled_bg_color};  /* Color de fondo cuando el botón está deshabilitado (gris) */
                color: {disabled_text_color};  /* Color del texto */
            }}
        """
        # Aplicar el estilo al botón
        button.setStyleSheet(style_sheet)

    def apply_text_box_styles(self, text_box, style_config):
        style_sheet = f"""
            QTextEdit{{
                background-color: {style_config.get('background-color', '#ffffff')};
                border: {style_config.get('border', '1px solid #ccc')};
                color: {style_config.get('color', '#000000')};
                font-size: {style_config.get('font-size', '12px')};
                font-family: {style_config.get('font-family', 'Arial')};
                border-radius: {style_config.get('border-radius', '0px')};
                padding: {style_config.get('padding', '0px')};  /* Espacio interno entre el borde y el texto */
            }}
            
            /* Hide Scrollbar */
            QScrollBar:vertical {{
                width: 0px;
                background: none;
            }}
            QScrollBar::handle:vertical {{
                background: none;
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                background: none;
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none;
            }}
        """

        text_box.setStyleSheet(style_sheet)
