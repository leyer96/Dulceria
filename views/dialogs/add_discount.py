from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QLabel,
    QDoubleSpinBox,
    QRadioButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
    QSpinBox,
    QButtonGroup
)
from PySide6.QtCore import Signal, Qt
from utils import Paths, get_expiration_date
import sqlite3

class AddDiscountDialog(QDialog):
    saved = Signal()
    def __init__(self, batch_id=None):
        super().__init__()

        self.batch_id = batch_id

        self.deal = False

        self.product_info_label = QLabel()
        self.product_info_label.setStyleSheet("font-size: 20px")

        subtitle1 = QLabel("Descuento")
        subtitle1.setStyleSheet("font-weight: bold")

        self.price_option = QRadioButton("Precio descuento: ")
        self.price_option.setChecked(True)
        self.price_input = QDoubleSpinBox()
        self.price_input.setMinimum(0)
        self.price_input.setSingleStep(1)
        
        price_layout = QHBoxLayout()
        price_layout.addWidget(self.price_option)
        price_layout.addWidget(self.price_input)

        self.percentage_option = QRadioButton("Porcentaje descuento (%)")
        self.percentage_input = QDoubleSpinBox()
        self.percentage_input.setRange(0, 100)
        self.percentage_input.setSingleStep(1)
        self.percentage_input.setEnabled(False)

        percentage_layout = QHBoxLayout()
        percentage_layout.addWidget(self.percentage_option)
        percentage_layout.addWidget(self.percentage_input)

        discount_mode_button_group = QButtonGroup(self)
        discount_mode_button_group.setExclusive(True)
        discount_mode_button_group.addButton(self.price_option)
        discount_mode_button_group.addButton(self.percentage_option)

        subtitle2 = QLabel("Vigencia")
        subtitle2.setStyleSheet("font-weight: bold")

        self.duration_input = QSpinBox()
        self.duration_input.setRange(1, 30)

        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Duración (días)"))
        duration_layout.addWidget(self.duration_input)
        
        self.redeems_input = QSpinBox()
        self.redeems_input.setRange(1, 999)

        redeems_layout = QHBoxLayout()
        redeems_layout.addWidget(QLabel("Canjes"))
        redeems_layout.addWidget(self.redeems_input)


        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(self.product_info_label)
        layout.addWidget(subtitle1)
        layout.addLayout(price_layout)
        layout.addLayout(percentage_layout)
        layout.addWidget(subtitle2)
        layout.addLayout(duration_layout)
        layout.addLayout(redeems_layout)
        layout.addWidget(button_box)

        layout.setAlignment(subtitle1, Qt.AlignHCenter)
        layout.setAlignment(subtitle2, Qt.AlignHCenter)

        self.setLayout(layout)

        button_box.accepted.connect(self.handle_accept)
        button_box.rejected.connect(self.close)
        self.price_option.toggled.connect(lambda: self.price_input.setEnabled(not self.price_input.isEnabled()))
        self.price_option.toggled.connect(lambda: self.percentage_input.setEnabled(not self.percentage_input.isEnabled()))

        self.get_product_data()

    
    def get_product_data(self):
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        try:
            product_id = cur.execute("SELECT product_id FROM batch WHERE id = ?", (self.batch_id,)).fetchone()[0]
            self.product_id = product_id
            r = cur.execute("SELECT name, brand, price FROM product WHERE id = ?", (product_id,)).fetchone()
            deal = cur.execute("SELECT * FROM deal WHERE product_id = ?", (product_id,)).fetchone()
            if deal:
                self.deal = True
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(self, "Error", "Ha ocurrido un error. Comuníquese con el administrador.")
        else:
            name = r[0]
            brand = r[1]
            price = r[2]
            self.price_input.setMaximum(price)
            self.product_info_label.setText(f"{brand} {name} - ${price}")
            self.price = price

    def handle_accept(self):
        if not self.deal:
            if self.price_option.isChecked():
                new_price = self.price_input.value()
            else:
                percentage = self.percentage_input.value()
                new_price =  self.price - (self.price * percentage / 100)
            if new_price:
                duration = self.duration_input.value()
                redeems = self.redeems_input.value()
                con = sqlite3.connect(Paths.test("db.db"))
                # con = sqlite3.connect(Paths.db())
                cur = con.cursor()
                expiration_date = get_expiration_date(duration)
                try:
                    cur.execute("""
                                INSERT INTO discount (product_id, price, expiration_date, redeems) VALUES (?, ?, ?, ?)
                                """, (self.product_id, new_price, expiration_date, redeems))
                except sqlite3.IntegrityError as e:
                    print(e)
                    QMessageBox.warning(self, "Error", "Ya existe un descuento para este producto.")
                except sqlite3.Error as e:
                    print(e)
                    QMessageBox.critical(self, "Error", "Ha ocurrido un error. Comuníquese con el administrador.")
                else:
                    con.commit()
                    self.close()
            else:
                QMessageBox.information(self, "Datos inválidos", "Ingrese un monto válido.")
        else:
            QMessageBox.information(self, "Error", "Ya hay una promoción para este producto")
        
