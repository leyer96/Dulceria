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
    def __init__(self, product_data, stock_id):
        super().__init__()

        self.product_id = product_data["product_id"]
        self.stock_id = stock_id

        if product_data["type"] == "Granel":
            product_label = QLabel(f"{product_data['brand']} {product_data['product']} (gr.)")
        else:
            product_label = QLabel(f"{product_data['brand']} {product_data['product']}")
        self.amount_input = QSpinBox()
        self.amount_input.setRange(0, 9999)
        self.amount_input.setSingleStep(1)
        amount = product_data["amount"]
        if type(amount) == str:
            amount = float(amount.split()[0])
        self.amount_input.setValue(amount)

        button_box = QDialogButtonBox(QDialogButtonBox.Save | QDialogButtonBox.Cancel)

        cancel_btn = button_box.button(QDialogButtonBox.Cancel)
        cancel_btn.setText("Cancelar")

        save_btn = button_box.button(QDialogButtonBox.Save)
        save_btn.setText("Guardar")

        button_box.accepted.connect(self.update_stock)
        button_box.rejected.connect(self.close)

        layout = QVBoxLayout()
        layout.addWidget(product_label)
        layout.addWidget(self.amount_input)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def update_stock(self):
        print("UPDATING STOCK")
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        amount = self.amount_input.value()
        query = "UPDATE stock SET amount = ? WHERE id = ?"
        print(f"AMOUNT {amount}; STOCK ID {self.stock_id}" )
        try:
            cur.execute(query, (amount, self.stock_id))
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(self, "Error", "Ha ocurrido un error. Contacte al administrador")
        else:
            con.commit()
            self.saved.emit()
            self.close()



