from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QSize
import qtawesome as qta


class ValveIndicator(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar el layout
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Centrar los widgets

        # Crear QPushButton para el LED
        self.led_button = QPushButton(self)
        self.led_button.setFixedSize(55, 55)  # Tamaño del botón
        self.led_button.setIconSize(QSize(45, 45))  # Tamaño del icono
        self.set_led_state(False)  # Estado inicial: apagado

        # Crear botón para cambiar el estado del LED
        self.toggle_button = QPushButton("Toggle LED", self)
        self.toggle_button.clicked.connect(self.toggle_led_state)

        # Añadir botones al layout
        layout.addWidget(self.led_button)
        layout.addWidget(self.toggle_button)

        self.setLayout(layout)

        # Establecer tamaño fijo para la ventana
        self.setFixedSize(300, 200)

        # Estado actual del LED (False para apagado, True para encendido)
        self.led_on = False

    def set_led_state(self, is_on):
        """Configura el color del LED y el estilo del botón dependiendo del estado."""
        if is_on:
            self.led_button.setIcon(
                qta.icon("mdi.lightbulb-cfl", color="white")
            )  # Icono de bombilla encendida
            self.led_button.setStyleSheet(
                """
                QPushButton {
                    background-color: #0be81b;
                    border: none;  /* Sin borde */
                    border-radius: 27px;  /* Radio para hacerlo redondo */
                }
                QPushButton:pressed {
                    border-style: inset;
                }
                """
            )
        else:
            self.led_button.setIcon(
                qta.icon("mdi.lightbulb-cfl-off", color="gray")
            )  # Icono de bombilla apagada
            self.led_button.setStyleSheet(
                """
                QPushButton {
                    background-color: darkgray;
                    border: none;  /* Sin borde */
                    border-radius: 27px;  /* Radio para hacerlo redondo */
                }
                QPushButton:pressed {
                    border-style: inset;
                }
                """
            )

    def toggle_led_state(self):
        """Alterna el estado del LED entre encendido y apagado."""
        self.led_on = not self.led_on
        self.set_led_state(self.led_on)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Crear una instancia del indicador de válvula
    window = ValveIndicator()
    window.show()

    sys.exit(app.exec())
