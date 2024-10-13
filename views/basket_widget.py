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

        # PROPS
        self.selected_row = None


