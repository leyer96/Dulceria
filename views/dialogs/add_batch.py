from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QFormLayout,
    QSpinBox,
    QDateEdit,
    QVBoxLayout,
    QComboBox,
    QRadioButton,
    QLineEdit
)
from PySide6.QtCore import QDate, QLocale, Signal, Qt
from utils import Paths
import sqlite3

class AddBatchDialog(QDialog):
    saved = Signal()
    error = Signal()
    def __init__(self):
        super().__init__()

        self.codes = []

        self.product_input = QComboBox()
        self.product_input.addItem("")
        self.product_input.setEditable(True)

        self.code_input = QLineEdit()
        
        self.amount_input = QSpinBox()
        self.amount_input.setRange(0,9999)
        self.amount_input.setSingleStep(1)

        self.expiration_date_input = QDateEdit(minimumDate=QDate.currentDate(), calendarPopup=True)
        self.expiration_date_input.calendarWidget().setLocale(QLocale.Spanish)

        self.no_exipration_option = QRadioButton()
        
        form = QFormLayout()
        form.addRow("Producto:", self.product_input)
        form.addRow("Código:", self.code_input)
        form.addRow("Cantidad:", self.amount_input)
        form.addRow("Fecha de Caducidad:", self.expiration_date_input)
        form.addRow("Sin caducidad", self.no_exipration_option)

        self.message_label = QLabel()

        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)

        button_box.rejected.connect(self.close)
        button_box.accepted.connect(self.validate_input)
        self.no_exipration_option.toggled.connect(self.toggle_date_input)
        self.code_input.textChanged.connect(self.search_product_by_code)
        
        self.message_label.hide()
        self.message_label.setStyleSheet("color: red;")
        self.populate_product_input()

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

    def populate_product_input(self):
        con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        products = cur.execute("SELECT id, name, code from product_test")
        names = []
        ids = []
        for product in products:
            ids.append(product[0])
            names.append(product[1])
            self.codes.append(product[2])
        self.product_input.addItems(names)
        self.names = names
        self.ids = ids

    def search_product_by_code(self, code):
        if code in self.codes:
            print("CODE MATCH")
            index = self.codes.index(code)
            self.product_input.setCurrentIndex(index + 1)
    
    def toggle_date_input(self):
        if self.no_exipration_option.isChecked():
            self.expiration_date_input.setEnabled(False)
        else:
            self.expiration_date_input.setEnabled(True)
    
    def validate_input(self):
        self.message_label.hide()
        product = self.product_input.currentText()
        amount = self.amount_input.value()
        code = self.code_input.text()
        msgs = []
        if product not in self.names:
            msgs.append("SELECCIONE UN PRODUCTO DENTRO DE LAS OPCIONES.")
        if amount == 0:
            msgs.append("SELECCIONE UNA CANTIDAD VÁLIDA.")
        if len(msgs) > 0:
            self.message_label.setText("\n".join(msgs))
            self.message_label.show()
        else:
            self.save()

    def save(self):
        con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        product_index = self.product_input.currentIndex() - 1
        product = self.product_input.currentText()
        product_id = self.ids[product_index]
        amount = self.amount_input.value()
        date_str = self.expiration_date_input.date().toString("yyyy-MM-dd")
        try:
            stock_id = cur.execute("SELECT id FROM stock_test WHERE product_id = ?", (product_id,)).fetchone()[0]
            try:
                prev_amount = cur.execute("SELECT amount from stock_test WHERE stock_test.product_id = ?", (product_id,)).fetchone()[0]
                new_amount = prev_amount + amount
                cur.execute("UPDATE stock_test SET amount = ? WHERE stock_test.product_id = ?", (new_amount, product_id))
                cur.execute(""" 
                    INSERT INTO batch_test (product_id, stock_id, product, amount, expiration_date) VALUES (?, ?, ?, ?, ?)
                    """, (product_id, stock_id, product, amount, date_str))
            except sqlite3.Error as e:
                print(e)
                self.message_label.setText("Ha ocurrido un error. Contacte al administrador.")
            else:
                con.commit()
                self.saved.emit()
                self.close()
        except sqlite3.Error as e:
            print(e)
            self.message_label.setText("Ha ocurrido un error. Contacte al administrador.")
        
