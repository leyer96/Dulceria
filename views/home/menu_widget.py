from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.add_btn = QPushButton("Agregar Nuevo Producto")
        self.go_to_list_btn = QPushButton("Productos")

        layout = QVBoxLayout()
        layout.addWidget(self.add_btn)
        layout.addWidget(self.go_to_list_btn)

        self.setLayout(layout)