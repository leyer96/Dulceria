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
    QLineEdit,
    QHBoxLayout
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

        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Código:"))
        search_layout.addWidget(self.code_input)
        search_layout.addWidget(QLabel("Nombre:"))
        search_layout.addWidget(self.product_input)
        
        form = QFormLayout()
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
        layout.addLayout(search_layout)
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
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        products = cur.execute("SELECT id, name, brand, code from product")
        display_names = []
        ids = []
        for product in products:
            ids.append(product[0])
            display_names.append(f"{product[2]} {product[1]}")
            self.codes.append(product[2])
        self.product_input.addItems(display_names)
        self.display_names = display_names
        self.ids = ids

    def search_product_by_code(self, code):
        if code in self.codes:
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
        msgs = []
        if product not in self.display_names:
            msgs.append("SELECCIONE UN PRODUCTO DENTRO DE LAS OPCIONES.")
        if amount == 0:
            msgs.append("SELECCIONE UNA CANTIDAD VÁLIDA.")
        if len(msgs) > 0:
            self.message_label.setText("\n".join(msgs))
            self.message_label.show()
        else:
            self.save()

    def save(self):
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        product_index = self.product_input.currentIndex() - 1
        product = self.product_input.currentText()
        product_id = self.ids[product_index]
        amount = self.amount_input.value()
        date_str = self.expiration_date_input.date().toString("yyyy-MM-dd")
        try:
            stock_id = cur.execute("SELECT id FROM stock WHERE product_id = ?", (product_id,)).fetchone()[0]
            try:
                prev_amount = cur.execute("SELECT amount from stock WHERE stock.product_id = ?", (product_id,)).fetchone()[0]
                new_amount = prev_amount + amount
                cur.execute("UPDATE stock SET amount = ? WHERE stock.product_id = ?", (new_amount, product_id))
                cur.execute(""" 
                    INSERT INTO batch (product_id, stock_id, product, amount, expiration_date) VALUES (?, ?, ?, ?, ?)
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
        
