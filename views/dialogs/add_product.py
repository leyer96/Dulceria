from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QDialogButtonBox,
    QRadioButton,
)
from PySide6.QtCore import Signal, Qt
from utils import Paths
import sqlite3


class AddItemDialog(QDialog):
    saved = Signal()
    def __init__(self, db, categories):
        super().__init__()

        self.db = db

        self.categories = categories

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.brand_input = QLineEdit()
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0,9999)
        self.buy_price_option = QRadioButton()
        self.buy_price_input = QDoubleSpinBox()
        self.buy_price_input.setRange(0,9999)
        self.category_input = QComboBox()
        self.category_input.addItems(categories)
        self.code_input = QLineEdit()
        form.addRow("Producto*", self.name_input)
        form.addRow("Marca", self.brand_input)
        form.addRow("Precio de venta*", self.price_input)
        form.addRow("Agregar precio de compra", self.buy_price_option)
        form.addRow("Precio de compra", self.buy_price_input)
        form.addRow("Categoría*", self.category_input)
        form.addRow("Código", self.code_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)

        cancel_btn = button_box.button(QDialogButtonBox.Cancel)
        cancel_btn.setText("Cancelar")

        save_btn = button_box.button(QDialogButtonBox.Save)
        save_btn.setText("Guardar")

        button_box.accepted.connect(self.validate_input)
        button_box.rejected.connect(self.close)

        self.message_label = QLabel()
        self.message_label.hide()
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet("color: red;")

        # CONFIG
        self.buy_price_input.setEnabled(False)
        # SIGNAL
        self.buy_price_option.toggled.connect(lambda: self.buy_price_input.setEnabled(not self.buy_price_input.isEnabled()))

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.message_label)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            event.accept() 
        else:
            super().keyPressEvent(event)
    
    def validate_input(self):
        self.message_label.hide()
        error_message = []
        name = self.name_input.text().strip().lower()
        brand = self.brand_input.text().strip().lower()
        price = self.price_input.value()
        category = self.category_input.currentText()
        code = self.code_input.text().strip()
        buy_price = self.buy_price_input.value()
        if not name:
            error_message.append("Agregue el nombre del producto")
        if price == 0:
            error_message.append("Agregue el precio del producto")
        if category != self.categories[0]:
            error_message.append("Seleccione una categoría")
        if self.buy_price_option.isChecked():
            if buy_price == 0:
                error_message.append("Agregue una precio de compra o deshabilite la opción.")
        if not error_message:
            name = name.lower()
            brand= brand.lower()
            item_data = {
                "name": name,
                "brand": brand,
                "price": price,
                "buy_price": buy_price,
                "category": category,
                "code": code
            }
            self.add_item(item_data)
        else:
            self.message_label.setText("\n".join(error_message))
            self.message_label.show()

    def add_item(self, item_data):
        name = item_data["name"]
        brand = item_data["brand"]
        price = item_data["price"]
        buy_price = item_data["buy_price"]
        category = item_data["category"]
        code = item_data["code"]
        if not code:
            code = None
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        try:
            cur.execute("""
                INSERT INTO product (name, brand, price, category, code, buy_price) VALUES(?,?,?,?,?,?)
            """, (name, brand, price, category, code, buy_price))
            con.commit()
        except sqlite3.IntegrityError as e:
            print(e)
            self.message_label.setText("Ya existe un producto con este nombre o código. Modifique el producto o elimínelo.")
            self.message_label.show()
        except sqlite3.Error as e:
            self.message_label.setText("Ha ocurrido un error. Contacte al desarrollador")
        else:
            product_id = cur.lastrowid
            try:
                cur.execute("""
                    INSERT INTO stock (product_id, product)
                    VALUES(?, ?)
                """, (product_id, name))
            except sqlite3.Error as e:
                print(e)
                self.message_label.setText("Ha habido un error al generar stock. Intente de nuevo. Si el problema persiste, contacte al administratodr.")
                self.message_label.show()
            else:
                con.commit()
                self.saved.emit()
                self.close()

