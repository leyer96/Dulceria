from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QDialogButtonBox,
    QMessageBox,
)
from PySide6.QtCore import Signal
from PySide6.QtSql import QSqlQuery
import sqlite3
from utils import Paths


class AddItemDialog(QDialog):
    saved = Signal()
    def __init__(self, db):
        super().__init__()

        self.db = db

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0,9999)
        self.category_input = QComboBox()
        self.category_input.addItems(["-- SELECCIONAR --","Dulce", "Chocolate", "Papas", "Desechable", "Decoración", "Piñata"])
        self.code_input = QLineEdit()
        form.addRow("Nombre", self.name_input)
        form.addRow("Precio", self.price_input)
        form.addRow("Categoría", self.category_input)
        form.addRow("Código", self.code_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        button_box.accepted.connect(self.validate_input)
        button_box.rejected.connect(self.close)

        self.message_label = QLabel()
        self.message_label.hide()
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("color: red;")

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.message_label)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def validate_input(self):
        self.message_label.hide()
        name = self.name_input.text()
        price = self.price_input.value()
        category = self.category_input.currentText()
        code = self.code_input.text()
        if name and price > 0 and category != "-- SELECCIONAR --":
            name = name.capitalize()
            item_data = {
                "name": name,
                "price": price,
                "category": category,
                "code": code
            }
            self.add_item(item_data)
        else:
            error_message = ""
            if not name:
                error_message += "\n Agregue un nombre."
            if price == 0:
                error_message += "\n Agregue un precio."
            if category == "-- SELECCIONAR --":
                error_message += "\n Seleccione una categoría"
            self.message_label.setText(error_message)
            self.message_label.show()

    def add_item(self, item_data):
        name = item_data["name"]
        price = item_data["price"]
        category = item_data["category"]
        code = item_data["code"]
        if not code:
            code = None
        con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO product_test (name, price, category, code) VALUES(?,?,?,?)
            """, (name, price, category, code))
            con.commit()
        except:
            self.message_label.setText("Ya existe un producto con este nombre. Modifique el producto o elimínelo.")
            self.message_label.show()
        else:
            product_id = cur.lastrowid
            try:
                cur.execute("""
                    INSERT INTO stock_test (product_id, product)
                    VALUES(?, ?)
                """, (product_id, name))
                con.commit()
            except:
                self.message_label.setText("Ha habido un error al generar stock. Intente de nuevo. Si el problema persiste, contacte al administratodr.")
                self.message_label.show()
            else:
                self.saved.emit()
                self.close()

