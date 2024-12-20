from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QSpinBox,
    QLabel,
    QVBoxLayout,
    QMessageBox
)
from PySide6.QtCore import Signal
from utils import Paths
import sqlite3

class EditStockDialog(QDialog):
    saved = Signal()
    def __init__(self, product_data):
        super().__init__()

        self.product_id = product_data["product_id"]

        product_label = QLabel(f"{product_data['brand']} {product_data['product']}")
        self.amount_input = QSpinBox()
        self.amount_input.setRange(0, 9999)
        self.amount_input.setSingleStep(1)
        self.amount_input.setValue(product_data["amount"])

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        button_box.accepted.connect(self.update_stock)
        button_box.rejected.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(product_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def update_stock(self):
        con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        amount = self.amount_input.value()
        query = "UPDATE stock_test SET amount = ? WHERE id = ?"
        try:
            cur.execute(query, (amount, self.product_id))
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(self, "Error", "Ha ocurrido un error. Contacte al administrador")
        else:
            con.commit()
            self.saved.emit()
            self.close()



