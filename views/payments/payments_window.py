from PySide6.QtWidgets import (
    QWidget,
    QTableView,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QAbstractItemView,
    QHeaderView,
    QGridLayout
)
from views.home.menu_widget import Menu
from views.home.search_widget import SearchWidget
from models.payment_model import PaymentModel

class PaymentsWindow(QWidget):
        def __init__(self, db):
            super().__init__()
            self.db = db
            self.search_widget = SearchWidget()
            self.menu = Menu()
            self.table = QTableView()
            self.model = PaymentModel(db)
            self.table.setModel(self.model)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table.setSelectionMode(QAbstractItemView.SingleSelection)
            self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

            # PASAR METODOS A WIDGET MENU
            # self.menu.go_to_add_product_btn.clicked.connect(self.open_add_dialog)

            grid = QGridLayout()

            grid.addWidget(self.search_widget, 0, 0, 2, 12)
            grid.addWidget(self.table, 2, 0, 5, 10)
            grid.addWidget(self.menu, 2, 11, 5, 1)

            self.menu.go_to_payments_list_btn.hide()

            self.setLayout(grid)