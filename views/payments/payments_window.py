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
from views.home.search_widget import SearchWidget
from models.payment_model import PaymentModel

class PaymentsWindow(QWidget):
        def __init__(self, db, menu):
            super().__init__()
            
            self.db = db
            self.menu = menu
            self.search_widget = SearchWidget()
            self.table = QTableView()
            self.model = PaymentModel(db)

            self.table.setModel(self.model)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table.setSelectionMode(QAbstractItemView.SingleSelection)
            self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
            # CONFIG
            self.menu.go_to_payments_btn.hide()
            
            # LAYOUT
            grid = QGridLayout()
            grid.addWidget(self.search_widget, 0, 0, 2, 12)
            grid.addWidget(self.table, 2, 0, 10, 9)
            grid.addWidget(self.menu, 2, 9, 5, 3)
            self.setLayout(grid)