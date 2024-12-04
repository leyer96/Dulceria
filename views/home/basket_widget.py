from PySide6.QtWidgets import (
    QWidget,
    QTableView,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QAbstractItemView,
    QHeaderView
    )
from PySide6.QtCore import Qt
from models.basket_model import BasketModel
from views.dialogs.set_amount import SetAmountDialog

class BasketWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.model = BasketModel()

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setStyleSheet("border: none")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        l1 = QLabel("Carrito")
        l2 = QLabel("TOTAL")

        self.amount_label = QLabel("$0")

        del_btn = QPushButton("Eliminar")
        edit_btn = QPushButton("Editar")
        confirm_btn = QPushButton("Cobrar")

        # LAYOUT

        layout = QHBoxLayout()

        btns_layout = QHBoxLayout()
        btns_layout.addWidget(del_btn)
        btns_layout.addWidget(edit_btn)
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(l1)
        left_layout.addWidget(self.table)
        left_layout.addLayout(btns_layout)

        left_container = QWidget()
        left_container.setLayout(left_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(l2)
        right_layout.addWidget(self.amount_label)
        right_layout.addWidget(confirm_btn)
        right_layout.setAlignment(l2, Qt.AlignHCenter)
        right_layout.setAlignment(self.amount_label, Qt.AlignHCenter)
        right_layout.setAlignment(confirm_btn, Qt.AlignHCenter)

        right_container = QWidget()
        right_container.setLayout(right_layout)
    
        layout.addWidget(left_container, stretch = 8)
        layout.addWidget(right_container, stretch = 4)

        self.setLayout(layout)        

        # SIGNALS
        self.model.total.connect(lambda total: self.amount_label.setText("${}".format(total)))
        self.table.clicked.connect(self.on_clicked_row)
        edit_btn.clicked.connect(self.select_amount)
        del_btn.clicked.connect(self.delete_item)

        # PROPS
        self.selected_row = None
        
    def on_clicked_row(self, index):
        self.selected_row = index.row()

    def select_amount(self):
        row = self.selected_row
        if row != None:
            product = self.model._data[row][1]
            amount = self.model._data[row][3]
            dlg = SetAmountDialog(product, amount)
            dlg.amount.connect(lambda amount: self.update_amount(row, amount))
            dlg.exec()

    def update_amount(self, row, amount):
        self.model._data[row][3] = amount
        self.model.calculate_total()
        self.model.layoutChanged.emit()

    def delete_item(self, row):
        row = self.selected_row
        if row != None:
            del(self.model._data[row])
            self.model.calculate_total()
            self.model.layoutChanged.emit()


