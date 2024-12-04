from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QDialogButtonBox,
)

from PySide6.QtSql import QSqlQuery

class AddItemDialog(QDialog):
    def __init__(self, db):
        super().__init__()

        self.db = db

        form = QFormLayout()
        self.name_input = QLineEdit()
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(0,9999)
        self.category_input = QComboBox()
        self.category_input.addItems(["-- SELECCIONAR --","Dulce", "Chocolate", "Papas", "Desechable", "Decoración", "Piñata"])
        form.addRow("Nombre", self.name_input)
        form.addRow("Precio", self.price_input)
        form.addRow("Categoría", self.category_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        button_box.accepted.connect(self.validate_input)
        button_box.rejected.connect(self.close)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def validate_input(self):
        name = self.name_input.text()
        price = self.price_input.value()
        category = self.category_input.currentText()
        if name and price > 0 and category != "-- SELECCIONAR --":
            name = name.capitalize()
            item_data = {
                "name": name,
                "price": price,
                "category": category
            }
            self.add_item(item_data)
        # ---- AGREGAR MENSAJE DE FORMULARIO INVÁLIDO ----

    def add_item(self, item_data):
        name = item_data["name"]
        price = item_data["price"]
        category = item_data["category"]
        # ----- USAR SQLITE ??? -----
        query = QSqlQuery(db=self.db)
        query.prepare("""
            INSERT INTO product_test (name, price, category, code) VALUES(?,?,?,?)
        """)
        query.addBindValue(name)
        query.addBindValue(price)
        query.addBindValue(category)
        query.addBindValue(None)
        # ----- USAR SQLITE ??? -----
        success = query.exec()
        if success:
            self.close()
        else:
            # ----- AGREGAR DIÁLOGO DE ERROR -----
            print("ERROR")

