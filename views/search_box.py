from PySide6.QtWidgets import (
    QAbstractItemView,
    QTableView,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QHeaderView
)
from PySide6.QtGui import QPalette, QColor
from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt, Signal
from utils import Paths
from views.dialogs.set_amount import SetAmountDialog

class SearchBox(QWidget):
    item_data = Signal(list)
    def __init__(self, db):
        super().__init__()

        self.db = db

        self.model = QSqlQueryModel()

        self.model.setHeaderData(0, Qt.Horizontal, "Id")
        self.model.setHeaderData(1, Qt.Horizontal, "Product")
        self.model.setHeaderData(2, Qt.Horizontal, "Price")

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setStyleSheet("border: none")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        add_btn = QPushButton("Agregar")
        edit_btn = QPushButton("Editar")

        # LAYOUT

        layout = QVBoxLayout()

        btns_layout = QHBoxLayout()
        btns_layout.addWidget(edit_btn)
        btns_layout.addWidget(add_btn)

        layout.addWidget(self.table)
        layout.addLayout(btns_layout)

        # SIGNALS
        self.table.clicked.connect(self.on_clicked_row)
        add_btn.clicked.connect(self.select_amount)

        # PROPS
        self.selected_row = None

        # WIDGET BACKGROUND WHITE
        # palette = self.palette()
        # palette.setColor(QPalette.Window, QColor("white"))
        # self.setAutoFillBackground(True)
        # self.setPalette(palette)

        self.setLayout(layout)

    def search(self, search_data):
        str = search_data[0]
        filter = search_data[1]
        query = """
            SELECT id, name, price FROM product_test
            WHERE {} LIKE '%{}%'
        """.format(filter, str)
        Qquery = QSqlQuery(query, db=self.db)
        r = self.model.setQuery(Qquery)
        print(r)

    def on_clicked_row(self, index):
        self.selected_row = index.row()
    
    def select_amount(self):
        row = self.selected_row
        if row != None:
            product = self.model.data(self.model.index(row, 1))
            dlg = SetAmountDialog(product)
            dlg.amount.connect(self.emit_item_data)
            dlg.exec()

    def emit_item_data(self, amount):
        row = self.selected_row
        id = self.model.data(self.model.index(row, 0))
        product = self.model.data(self.model.index(row, 1))
        price = self.model.data(self.model.index(row, 2))
        item_data = [id, product, price, amount]
        self.item_data.emit(item_data)