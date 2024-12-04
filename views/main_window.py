from PySide6.QtWidgets import QMainWindow, QStackedLayout, QWidget
from views.home.home_window import HomeWindow
from views.products.products_window import ProductsWindow
from views.payments.payments_window import PaymentsWindow

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()

        self.resize(700, 500)

        home_window = HomeWindow(db)
        products_window = ProductsWindow(db)
        payments_window = PaymentsWindow(db)

        container = QWidget()
        container_layout = QStackedLayout()
        container_layout.addWidget(home_window)
        container_layout.addWidget(products_window)
        container_layout.addWidget(payments_window)
        container.setLayout(container_layout)

        home_window.menu.go_to_product_list_btn.clicked.connect(lambda: container_layout.setCurrentIndex(1))
        home_window.menu.go_to_payments_list_btn.clicked.connect(lambda: container_layout.setCurrentIndex(2)) # ELIMINAR -> BOTON PARA OBTENER TODOS LOS REGISTROS
        home_window.menu.go_to_product_list_btn.clicked.connect(products_window.model.get_all_prodcuts) # ELIMINAR -> BOTON PARA OBTENER TODOS LOS REGISTROS
        home_window.menu.go_to_payments_list_btn.clicked.connect(payments_window.model.get_all_payments) # ELIMINAR -> BOTON PARA OBTENER TODOS LOS REGISTROS

        products_window.menu.go_to_home_btn.clicked.connect(lambda: container_layout.setCurrentIndex(0))

        payments_window.menu.go_to_home_btn.clicked.connect(lambda: container_layout.setCurrentIndex(0))
        
        
        self.setCentralWidget(container)
        self.show()