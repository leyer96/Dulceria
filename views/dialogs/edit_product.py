from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QLabel,
    QDialogButtonBox,
    QMessageBox
)
from PySide6.QtCore import Signal
from utils import Paths
import sqlite3

class EditItemDialog(QDialog):
    item_edited = Signal()
    def __init__(self, db, product_id, categories):
        super().__init__()

        self.db = db

        self.product_id = str(product_id)
        self.categories = categories

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.brand_input = QLineEdit()
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0,9999)
        self.category_input = QComboBox()
        self.category_input.addItems(categories)
        self.code_input = QLineEdit()
        form.addRow("Nombre", self.name_input)
        form.addRow("Marca", self.brand_input)
        form.addRow("Precio", self.price_input)
        form.addRow("Categoría", self.category_input)
        form.addRow("Código", self.code_input)

        self.msgs_label = QLabel()

        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)

        cancel_btn = button_box.button(QDialogButtonBox.Cancel)
        cancel_btn.setText("Cancelar")

        save_btn = button_box.button(QDialogButtonBox.Save)
        save_btn.setText("Guardar")

        button_box.accepted.connect(self.validate_input)
        button_box.rejected.connect(self.close)

        self.msgs_label.hide()
        self.msgs_label.setStyleSheet("color: red;")
        

        self.load_item_data()

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def load_item_data(self):
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        query = """
            SELECT * FROM product WHERE id = ?
        """
        try:
            product_data = cur.execute(query, (self.product_id,)).fetchone()
        except sqlite3.Error as e:
            print(e)
            QMessageBox.information(self, "Error en Búsqueda", "No se encontraron los datos correspondientes al producto.")
        else:        
            self.name_input.setText(product_data[1])
            self.brand_input.setText(product_data[2])
            self.price_input.setValue(product_data[3])
            self.category_input.setCurrentText(product_data[4])
            self.code_input.setText(product_data[5])

    def validate_input(self):
        self.msgs_label.hide()
        name = self.name_input.text()
        brand = self.brand_input.text()
        price = self.price_input.value()
        category = self.category_input.currentText()
        code = self.code_input.text()
        
        msgs= []
        if not name:
            msgs.append("Agregue el nombre del producto")
        if price == 0:
            msgs.append("Agregue un precio válido")
        if category == self.categories[0]:
            msgs.append("Seleccione una categoría válida")
        if len(msgs)== 0:
            name = name.lower()
            brand = brand.lower()
            item_data = {
                "name": name,
                "brand": brand,
                "price": price,
                "category": category,
                "code": code
            }
            self.save(item_data)

    def save(self, item_data):
        print(item_data)
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()

        name = item_data["name"]
        brand = item_data["brand"]
        price = item_data["price"]
        category = item_data["category"]
        code = item_data["code"]
        if not code:
            code = None
        query = """
            UPDATE product
            SET name = ?, brand = ?, price = ?, category = ?,code = ?
            WHERE id = ?
        """
        try:
            cur.execute(query, (name, brand, price, category, code, self.product_id))
        except sqlite3.Error as e:
            print(e)
            QMessageBox.information(self, "Error", "Ha habido un error al guardar los datos. Comuníquese con el administrador.")
        else:
            con.commit()
            self.item_edited.emit()
            self.close()
    
    
        
