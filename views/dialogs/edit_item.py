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
        self.name = QLineEdit()
        self.price = QDoubleSpinBox()
        self.price.setRange(0,9999)
        self.category = QComboBox()
        self.category.addItems(["-- SELECCIONAR --","Dulce", "Chocolate", "Papas", "Desechable", "Decoración", "Piñata"])
        self.code = QLineEdit()
        form.addRow("Nombre", self.name)
        form.addRow("Precio", self.price)
        form.addRow("Categoría", self.category)
        form.addRow("Código", self.code)

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
                self.name.setText(query.value(1))
                self.price.setValue(query.value(2))
                # self.category.setValue(query.value(#))
                self.code.setText(str(query.value(3)))
        else:
            print("ERROR")

    def validate_input(self):
        name = self.name.text()
        price = self.price.value()
        category = self.category.currentText()
        code = self.code.text()
        # if name and price > 0 and category != "-- SELECCIONAR --":
        if name and price > 0:
            # name = name.lower()
            item_data = [name, price, category, code]
            self.save(item_data)

    def save(self, item_data):
        name = item_data[0]
        price = item_data[1]
        # category = item_data[2]
        code = item_data[3]
        if not code:
            code = None
        query = QSqlQuery(db=self.db)
        query.prepare("""
            UPDATE product_test
            SET name = ?, price = ?, code = ?
            WHERE id = ?
        """)
        query.addBindValue(name)
        query.addBindValue(price)
        query.addBindValue(code)
        query.addBindValue(self.product_id)

        if query.exec():
            self.item_edited.emit()
            self.close()
        else:
            print(query.lastError().text())
    
    
        
