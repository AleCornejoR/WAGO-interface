from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt6.QtGui import QPixmap


class ValveIndicator(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar el layout
        layout = QVBoxLayout()

        # Crear QLabel para el LED
        self.led_label = QLabel(self)
        self.set_led_state(False)  # Estado inicial: apagado

        layout.addWidget(self.led_label)
        self.setLayout(layout)

    def set_led_state(self, is_on):
        if is_on:
            pixmap = QPixmap("green_led.png")  # Imagen del LED encendido
        else:
            pixmap = QPixmap("red_led.png")  # Imagen del LED apagado
        self.led_label.setPixmap(pixmap)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)

    # Crear una instancia del indicador de válvula
    window = ValveIndicator()
    window.show()

    sys.exit(app.exec())
