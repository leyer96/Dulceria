from PySide6.QtWidgets import QMainWindow, QStackedLayout, QWidget
from views.home.home_window import HomeWindow
from views.menu_widget import Menu
from views.products.products_window import ProductsWindow
from views.payments.payments_window import PaymentsWindow

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()

        self.resize(700, 500)
 
        windows = [HomeWindow, ProductsWindow, PaymentsWindow]

        container = QWidget()
        container_layout = QStackedLayout()

        for window in windows:
            menu = Menu()
            menu.go_to_home.connect(lambda: container_layout.setCurrentIndex(0))
            menu.go_to_products.connect(lambda: container_layout.setCurrentIndex(1))
            menu.go_to_payments.connect(lambda: container_layout.setCurrentIndex(2))
            w = window(db, menu)
            container_layout.addWidget(w)

        container.setLayout(container_layout)
        
        self.setCentralWidget(container)
        self.show()