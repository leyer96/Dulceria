from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QDialogButtonBox,
    QHBoxLayout
)
from PySide6.QtCore import Signal
from PySide6.QtSql import QSqlQuery

class EditItemDialog(QDialog):
    item_edited = Signal()
    def __init__(self, db, product_id):
        super().__init__()

        self.db = db

        self.product_id = product_id

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

        self.load_item_data()

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def load_item_data(self):
        query = QSqlQuery(db=self.db)
        query.prepare("""
            SELECT * FROM product_test WHERE id = (?)
        """)
        query.addBindValue(self.product_id)
        
        if query.exec():
            while query.next():
                self.name_input.setText(query.value(1))
                self.price_input.setValue(query.value(2))
                self.category_input.setCurrentText(query.value(3))
                self.code_input.setText(str(query.value(4)))
        else:
            print("ERROR")

    def validate_input(self):
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
            self.save(item_data)

    def save(self, item_data):
        name = item_data["name"]
        price = item_data["price"]
        category = item_data["category"]
        code = item_data["code"]
        if not code:
            code = None
        query = QSqlQuery(db=self.db)
        query.prepare("""
            UPDATE product_test
            SET name = ?, price = ?, category = ?,code = ?
            WHERE id = ?
        """)
        query.addBindValue(name)
        query.addBindValue(price)
        query.addBindValue(category)
        query.addBindValue(code)
        query.addBindValue(self.product_id)

        if query.exec():
            self.item_edited.emit()
            self.close()
        else:
            print(query.lastError().text())
    
    
        
