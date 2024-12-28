from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QRadioButton,
    QButtonGroup,
    QSpinBox,
    QDoubleSpinBox,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QMessageBox
)
from PySide6.QtCore import Signal, Qt
from utils import Paths, get_expiration_date
import sqlite3

class AddDealDialog(QDialog):
    saved = Signal()
    def __init__(self, batch_id):
        super().__init__()

        self.batch_id = batch_id

        self.discount = False

        # WIDGETS
        self.product_info_label = QLabel()
        self.product_info_label.setStyleSheet("font-size: 20px")

        subtitle1 = QLabel("Promoción")
        subtitle1.setStyleSheet("font-weight: bold")

        self.amountxamount_option = QRadioButton()
        self.first_amount_input = QSpinBox()
        self.first_amount_input.setRange(1,10)
        self.second_amount_input = QSpinBox()
        self.second_amount_input.setRange(1,10)

        self.amountxprice_option = QRadioButton()
        self.amount_input = QSpinBox()
        self.amount_input.setRange(1,10)
        self.price_input = QDoubleSpinBox()
        self.price_input.setRange(1,9999)

        deal_button_group = QButtonGroup(self)
        deal_button_group.addButton(self.amountxamount_option)
        deal_button_group.addButton(self.amountxprice_option)

        subtitle2 = QLabel("Vigencia")
        subtitle2.setStyleSheet("font-weight: bold")

        self.duration_input = QSpinBox()
        self.duration_input.setRange(1,30)
        self.duration_input.setValue(30)
        self.duration_input.setSingleStep(1)

        self.redeems_input = QSpinBox()
        self.redeems_input.setRange(1,100)
        self.redeems_input.setSingleStep(1)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        # SIGNALS
        button_box.accepted.connect(self.handle_accept)
        button_box.rejected.connect(self.close)

        # LAYOUT
        amountxamount_layout = QHBoxLayout()
        amountxamount_layout.addWidget(self.amountxamount_option)
        amountxamount_layout.addWidget(self.first_amount_input)
        amountxamount_layout.addWidget(QLabel(" x "))
        amountxamount_layout.addWidget(self.second_amount_input)

        amountxprice_layout = QHBoxLayout()
        amountxprice_layout.addWidget(self.amountxprice_option)
        amountxprice_layout.addWidget(self.amount_input)
        amountxprice_layout.addWidget(QLabel(" x "))
        amountxprice_layout.addWidget(self.price_input)

        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Duración (días): "))
        duration_layout.addWidget(self.duration_input)
        
        redeems_layout = QHBoxLayout()
        redeems_layout.addWidget(QLabel("Canjes: "))
        redeems_layout.addWidget(self.redeems_input)

        layout = QVBoxLayout()
        layout.addWidget(self.product_info_label)
        layout.addWidget(subtitle1)
        layout.addWidget(QLabel("Cantidad x Cantidad (3 x 2)"))
        layout.addLayout(amountxamount_layout)
        layout.addWidget(QLabel("Cantidad x Precio (2 x $20)"))
        layout.addLayout(amountxprice_layout)
        layout.addWidget(subtitle2)
        layout.addLayout(duration_layout)
        layout.addLayout(redeems_layout)
        layout.addWidget(button_box)

        layout.setAlignment(subtitle1, Qt.AlignHCenter)
        layout.setAlignment(subtitle2, Qt.AlignHCenter)

        self.setLayout(layout)

        # CONFIG
        self.amountxamount_option.setChecked(True)

        # LOAD
        self.get_product_data()
    
    def get_product_data(self):
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        try:
            product_id = cur.execute("SELECT product_id FROM batch WHERE id = ?", (self.batch_id,)).fetchone()[0]
            self.product_id = product_id
            r = cur.execute("SELECT name, brand, price FROM product WHERE id = ?", (product_id,)).fetchone()
            discount = cur.execute("SELECT * FROM discount WHERE product_id = ?", (product_id,)).fetchone()
            if discount:
                self.discount = True
        except sqlite3.Error as e:
            print(e)
            QMessageBox.critical(self, "Error", "Ha ocurrido un error. Comuníquese con el administrador.")
        else:
            name = r[0]
            brand = r[1]
            price = r[2]
            self.product_info_label.setText(f"{brand} {name} - ${price}")
            self.price = price

    def handle_accept(self):
        if not self.discount:
            con = sqlite3.connect(Paths.test("db.db"))
            # con = sqlite3.connect(Paths.db())
            cur = con.cursor()
            duration = self.duration_input.value()
            expiration_date = get_expiration_date(duration)
            redeems = self.redeems_input.value()
            if self.amountxamount_option.isChecked():
                first_amount = self.first_amount_input.value()
                second_amount = self.second_amount_input.value()
                if first_amount <= second_amount:
                    QMessageBox.information(self, "Datos inválidos", "Asegúrese que la primera cantidad sea mayor a la segunda.")
                else:
                    try:
                        cur.execute(
                            """
                            INSERT INTO deal (product_id, type, first_amount, second_amount, expiration_date, redeems) VALUES (?,?,?,?,?,?)
                            """, (self.product_id, 0, first_amount, second_amount, expiration_date, redeems))
                    except sqlite3.IntegrityError as e:
                        print(e)
                        QMessageBox.critical(self, "Error", "Ya existe una promoción para este producto")
                    except sqlite3.Error as e:
                        print(e)
                        QMessageBox.critical(self, "Error", "Ha ocurrido un error. Por favor contacte al administrador")
                    else:
                        con.commit()
                        QMessageBox.information(self, "Promoción Guardada", "Promoción guardada con éxito")
                        self.saved.emit()
                        self.close()
            else:
                amount = self.amount_input.value()
                price = self.price_input.value()
                if price/amount > self.price:
                    QMessageBox.information(self, "Datos inválidos", "El precio unitario de la promoción es mayor al precio normal.")
                else:
                    try:
                        cur.execute(
                            """
                            INSERT INTO deal (product_id, type, amount, price, expiration_date, redeems) VALUES (?,?,?,?,?,?)
                            """, (self.product_id, 1, amount, price, expiration_date, redeems))
                    except sqlite3.IntegrityError as e:
                        print(e)
                        QMessageBox.critical(self, "Error", "Ya existe una promoción para este producto")
                    except sqlite3.Error as e:
                        print(e)
                        QMessageBox.critical(self, "Error", "Ha ocurrido un error. Por favor contacte al administrador")
                    else:
                        con.commit()
                        QMessageBox.information(self, "Promoción Guardada", "Promoción guardada con éxito")
                        self.saved.emit()
                        self.close()
        else:
            QMessageBox.information(self, "Error", "Ya hay un descuento para este producto")


