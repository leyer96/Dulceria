from PySide6.QtWidgets import (
    QAbstractItemView,
    QTableView,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QHeaderView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QCursor
from utils import Paths
from views.dialogs.set_amount import SetAmountDialog
from views.dialogs.edit_product import EditItemDialog
from models.search_product_model import SearchModel

class SearchBox(QWidget):
    item_data = Signal(list)
    def __init__(self, db):
        super().__init__()

        self.db = db

        self.search_str = ""
        self.filter = None

        self.model = SearchModel(db)

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setStyleSheet("border: none")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.add_btn = QPushButton(QIcon(Paths.icon("shopping-basket--plus.png")),"Agregar")

        # LAYOUT
        layout = QVBoxLayout()

        btns_layout = QHBoxLayout()
        btns_layout.addWidget(self.add_btn)

        layout.addWidget(self.table)
        layout.addLayout(btns_layout)

        # SIGNALS
        self.table.clicked.connect(self.on_clicked_row)
        self.add_btn.clicked.connect(self.select_amount)

        # PROPS
        self.selected_row = None
        self.add_btn.setEnabled(False)
        self.add_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.setLayout(layout)

    def on_clicked_row(self, index):
        self.selected_row = index.row()
        if not self.add_btn.isEnabled():
            self.add_btn.setEnabled(True)
    
    def select_amount(self):
        row = self.selected_row
        if row != None:
            product = self.model.data(self.model.index(row, 1), Qt.DisplayRole)
            dlg = SetAmountDialog(product)
            dlg.float_amount.connect(self.emit_item_data)
            dlg.int_amount.connect(self.emit_item_data)
            dlg.exec()

    def emit_item_data(self, amount):
        row = self.selected_row
        id = self.model.data(self.model.index(row, 0), Qt.DisplayRole)
        product = self.model.data(self.model.index(row, 1), Qt.DisplayRole)
        brand = self.model.data(self.model.index(row, 2), Qt.DisplayRole)
        price = self.model.data(self.model.index(row, 3), Qt.DisplayRole)
        item_data = [id, product, brand, price, amount]
        self.item_data.emit(item_data)
        
