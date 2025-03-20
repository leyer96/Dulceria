from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QDialogButtonBox,
    QVBoxLayout
)
import sqlite3
from utils import Paths


class ViewPaymentDetailsDialog(QDialog):
    def __init__(self, payment_data):
        super().__init__()

        timestamp = payment_data["timestamp"]
        date = timestamp[0:10]
        time = timestamp[10:len(timestamp)]

        self.date_label = QLabel("Fecha: " + date)
        self.time_label = QLabel("Hora: " + time)
        self.quantity_label = QLabel("Cantidad: " + str(payment_data["amount"]))
        self.payment_form_label = QLabel("Forma de pago: " + payment_data["payment_form"])
        self.note_label = QLabel("Nota: " + payment_data["note"])
        l1 = QLabel("Productos: ")
        self.products_and_amount_label = QLabel()

        self.populate_labels(payment_data["id"])

        layout = QVBoxLayout()
        layout.addWidget(self.date_label)
        layout.addWidget(self.time_label)
        layout.addWidget(self.quantity_label)
        layout.addWidget(self.payment_form_label)
        layout.addWidget(l1)
        layout.addWidget(self.products_and_amount_label)
        layout.addWidget(self.note_label)

        self.setLayout(layout)

    def populate_labels(self, payment_id):
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        productpayments = cur.execute("""
            SELECT * FROM productpayment WHERE payment_id = ?
        """, (payment_id,)).fetchall()
        text_lines = []
        for productpayment in productpayments:
            product_name = productpayment[3]
            amount = productpayment[4]
            price = productpayment[5]
            text_lines.append("{} x {} - ${} c/u".format(product_name, amount, price))
        text = "\n".join(text_lines)
        self.products_and_amount_label.setText(text)





