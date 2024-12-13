from PySide6.QtWidgets import QMainWindow, QStackedLayout, QWidget
from views.home.home_window import HomeWindow
from views.menu_widget import Menu
from views.products.products_window import ProductsWindow
from views.payments.payments_window import PaymentsWindow
from views.stock.stock_window import StockWindow

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()

        self.resize(700, 500)
 
        windows = [HomeWindow, ProductsWindow, PaymentsWindow, StockWindow]
        initialized_window = []

        container = QWidget()
        container_layout = QStackedLayout()

        for window in windows:
            menu = Menu()
            menu.go_to_home.connect(lambda: container_layout.setCurrentIndex(0))
            menu.go_to_products.connect(lambda: container_layout.setCurrentIndex(1))
            menu.go_to_payments.connect(lambda: container_layout.setCurrentIndex(2))
            menu.go_to_stock.connect(lambda: container_layout.setCurrentIndex(3))
            w = window(db, menu)

            initialized_window.append(w)
            container_layout.addWidget(w)

        for i in range(0, len(initialized_window)):
            for j in range(0,len(initialized_window)):
                if i == j:
                    continue
                wi = initialized_window[i]
                wj = initialized_window[j]
                if isinstance(wi, StockWindow):
                    wj.menu.go_to_stock.connect(wi.stock_model.get_all_stock)
                    wj.menu.go_to_stock.connect(wi.batch_model.get_all_batchs)
                if isinstance(wi, PaymentsWindow):
                    wj.menu.go_to_payments.connect(wi.to_default)

        container.setLayout(container_layout)
        
        self.setCentralWidget(container)
        self.show()