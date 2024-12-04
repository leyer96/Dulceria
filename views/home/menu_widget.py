from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.go_to_add_product_btn = QPushButton("Agregar Nuevo Producto")
        self.go_to_product_list_btn = QPushButton("Productos")
        self.go_to_home_btn = QPushButton("Inicio")
        self.go_to_payments_list_btn = QPushButton("Pagos")
        self.go_to_admin_window_btn = QPushButton("Admin")


        layout = QVBoxLayout()
        layout.addWidget(self.go_to_home_btn)
        layout.addWidget(self.go_to_add_product_btn)
        layout.addWidget(self.go_to_product_list_btn)
        layout.addWidget(self.go_to_payments_list_btn)
        layout.addWidget(self.go_to_admin_window_btn)

        self.setLayout(layout)