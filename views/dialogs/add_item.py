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

from PySide6.QtSql import QSqlQuery

class AddItemDialog(QDialog):
    def __init__(self, db):
        super().__init__()

        self.db = db

        form = QFormLayout()
        self.name = QLineEdit()
        self.price = QDoubleSpinBox()
        self.price.setRange(0,9999)
        self.category = QComboBox()
        self.category.addItems(["-- SELECCIONAR --","Dulce", "Chocolate", "Papas", "Desechable", "Decoración", "Piñata"])
        form.addRow("Nombre", self.name)
        form.addRow("Precio", self.price)
        form.addRow("Categoría", self.category)

        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        button_box.accepted.connect(self.validate_input)
        button_box.rejected.connect(self.close)

        layout = QVBoxLayout()
        layout.addLayout(form)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def validate_input(self):
        name = self.name.text()
        price = self.price.value()
        category = self.category.currentText()
        if name and price > 0 and category != "-- SELECCIONAR --":
            # name = name.lower()
            item_data = [name, price, category]
            self.add_item(item_data)

    def add_item(self, item_data):
        name = item_data[0]
        price = item_data[1]
        # category = item_data[2]
        query = QSqlQuery(db=self.db)
        query.prepare("""
            INSERT INTO product_test (name, price, code) VALUES(?,?,?)
        """)
        query.addBindValue(name)
        query.addBindValue(price)
        query.addBindValue(None)

        query.exec()
        
        self.close()

