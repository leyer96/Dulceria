from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
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
        self.message_label.setStyleSheet("color: red;")

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(button_box)
        layout.addWidget(self.message_label)

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

        # ---- AGREGAR MENSAJE DE FORMULARIO INVÁLIDO ----

    def add_item(self, item_data):
        name = item_data["name"]
        price = item_data["price"]
        category = item_data["category"]
        code = item_data["code"]
        if not code:
            code = None
        # ----- USAR SQLITE ??? -----
        query = QSqlQuery(db=self.db)
        query.prepare("""
            INSERT INTO product_test (name, price, category, code) VALUES(?,?,?,?)
        """)
        query.addBindValue(name)
        query.addBindValue(price)
        query.addBindValue(category)
        query.addBindValue(code)
        # ----- USAR SQLITE ??? -----
        success = query.exec()
        if success:
            self.close()
        else:
            self.message_label.setText("Ha ocurrido un error. Intente de nuevo o contacte al administrador.")

