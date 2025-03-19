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
    QMessageBox
)
from PySide6.QtCore import Signal, Qt
from utils import Paths
import sqlite3


class AddItemDialog(QDialog):
    saved = Signal()
    def __init__(self, db, categories, product_id=None):
        super().__init__()

        self.db = db

        self.categories = categories

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.brand_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(categories)
        self.price_label = QLabel("Precio de venta*")
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0,9999)
        self.buy_price_option = QRadioButton()
        self.buy_price_input = QDoubleSpinBox()
        self.buy_price_input.setRange(0,9999)
        self.code_input = QLineEdit()
        form.addRow("Producto*", self.name_input)
        form.addRow("Marca", self.brand_input)
        form.addRow("Categoría*", self.category_input)
        form.addRow(self.price_label, self.price_input)
        form.addRow("Agregar precio de compra", self.buy_price_option)
        form.addRow("Precio de compra", self.buy_price_input)
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
        self.category_input.currentTextChanged.connect(self.update_price_text)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(self.message_label)
        layout.addWidget(button_box)

        self.setLayout(layout)

        self.action = "POST"
        if product_id:
            self.product_id = product_id
            self.action = "EDIT"
            self.populate_inputs(product_id)

    def populate_inputs(self, product_id):
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        query = """
            SELECT name,brand,price,buy_price,category,code FROM product WHERE id = ?
        """
        try:
            product_data = cur.execute(query, (product_id,)).fetchone()
        except sqlite3.Error as e:
            print(e)
            QMessageBox.information(self, "Error en Búsqueda", "No se encontraron los datos correspondientes al producto.")
        else:        
            self.name_input.setText(product_data[0])
            self.brand_input.setText(product_data[1])
            self.price_input.setValue(product_data[2])
            buy_price = product_data[3]
            if buy_price != 0:
                self.buy_price_option.setChecked(True)
                self.buy_price_input.setValue(product_data[3])
            self.category_input.setCurrentText(product_data[4])
            self.code_input.setText(product_data[5])
    
    def update_price_text(self, text):
        if text == "Granel":
            self.price_label.setText("Precio de venta (x gr.)*")
        else:
            self.price_label.setText("Precio de venta*")
    
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
        if category == self.categories[0]:
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
            if self.action == "POST":
                self.add_item(item_data)
            else:
                self.edit_item(item_data)
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
            print(e)
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
                self.message_label.setText("Ha habido un error al generar inventario para el producto. Contacte al administratodr.")
                self.message_label.show()
            else:
                con.commit()
                self.saved.emit()
                self.close()
                QMessageBox.information(self, "Producto Guardado", "El producto se ha agregado con éxito.")

    def edit_item(self, item_data):
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
                UPDATE product SET name = ?, brand = ?, price = ?, category = ?, code = ?, buy_price = ? WHERE id = ?
            """, (name, brand, price, category, code, buy_price, self.product_id))
            con.commit()
        except sqlite3.IntegrityError as e:
            print(e)
            self.message_label.setText("Ya existe un producto con este nombre o código. Intente con otro código de producto.")
            self.message_label.show()
        except sqlite3.Error as e:
            print(e)
            self.message_label.setText("Ha ocurrido un error. Contacte al desarrollador")
        else:
            con.commit()
            self.saved.emit()
            self.close()
            QMessageBox.information(self, "Producto Actualizado", "El producto se ha actualizado con éxito.")

