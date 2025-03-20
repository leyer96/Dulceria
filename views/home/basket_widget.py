from PySide6.QtWidgets import (
    QWidget,
    QTableView,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QLabel,
    QAbstractItemView,
    QHeaderView,
    QMessageBox
    )
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QCursor
from models.basket_model import BasketModel
from views.dialogs.update_amount import UpdateAmountDialog
from views.dialogs.register_payment import RegisterPaymentDialog
from utils import save_payment, Paths, substract_from_stock, update_discount, update_deal

class BasketWidget(QWidget):
    payment_saved = Signal()
    def __init__(self):
        super().__init__()

        self.model = BasketModel()

        self.table = QTableView()
        self.table.setModel(self.model)
        self.table.setStyleSheet("border: none")
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        l1 = QLabel("CARRITO")
        l2 = QLabel("TOTAL")

        self.amount_label = QLabel("$0")

        self.del_btn = QPushButton(QIcon(Paths.icon("shopping-basket--minus.png")),"Eliminar")
        # self.edit_btn = QPushButton(QIcon(Paths.icon("shopping-basket--pencil.png")),"Editar")
        confirm_btn = QPushButton(QIcon(Paths.icon("credit-card--plus.png")),"Cobrar")

        # CONFIG
        l1.setStyleSheet("font-size: 20px;")
        self.del_btn.setStyleSheet("height: 20px;")

        # LAYOUT
        layout = QHBoxLayout()

        btns_layout = QHBoxLayout()
        btns_layout.addWidget(self.del_btn)
        # btns_layout.addWidget(self.edit_btn)
        
        left_layout = QVBoxLayout()
        left_layout.addWidget(l1)
        left_layout.addWidget(self.table)
        left_layout.addLayout(btns_layout)

        left_container = QWidget()
        left_container.setLayout(left_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(l2)
        right_layout.addWidget(self.amount_label)
        right_layout.addWidget(confirm_btn)
        right_layout.setAlignment(l2, Qt.AlignHCenter)
        right_layout.setAlignment(self.amount_label, Qt.AlignHCenter)
        right_layout.setAlignment(confirm_btn, Qt.AlignHCenter)

        right_container = QWidget()
        right_container.setLayout(right_layout)
    
        layout.addWidget(left_container)
        layout.addWidget(right_container)

        layout.setStretch(0, 4)
        layout.setStretch(1, 1)

        self.setLayout(layout)        

        # SIGNALS
        self.model.total_calculated.connect(lambda total: self.amount_label.setText("${}".format(total)))
        self.model.layoutChanged.connect(lambda: self.del_btn.setEnabled(False))
        # self.model.layoutChanged.connect(lambda: self.edit_btn.setEnabled(False))
        self.model.layoutChanged.connect(self.table.clearSelection)
        self.model.deal_available.connect(lambda deal_str: QMessageBox.information(self, "Promoción Encotrada", f"Hay una promoción {deal_str} para este producto."))
        self.table.clicked.connect(self.on_clicked_row)
        # self.edit_btn.clicked.connect(self.select_amount)
        self.del_btn.clicked.connect(lambda: self.model.delete_item(self.selected_row))
        confirm_btn.clicked.connect(self.open_payment_dialog)

        # PROPS
        self.selected_row = None
        # self.edit_btn.setEnabled(False)
        # self.edit_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.del_btn.setEnabled(False)
        self.del_btn.setCursor(QCursor(Qt.PointingHandCursor))
        confirm_btn.setCursor(QCursor(Qt.PointingHandCursor))
        
    def on_clicked_row(self, index):
        self.selected_row = index.row()
        if not self.del_btn.isEnabled():
            # self.edit_btn.setEnabled(True)
            self.del_btn.setEnabled(True)

    def select_amount(self):
        row = self.selected_row
        if row != None:
            product = self.model._data[row][1]
            amount = self.model._data[row][4]
            dlg = UpdateAmountDialog(product, amount, True)
            dlg.int_amount.connect(lambda amount: self.update_amount(row, amount))
            dlg.float_amount.connect(lambda amount: self.update_amount(row, amount))
            dlg.exec()

    def update_amount(self, row, amount):
        self.model._data[row][4] = amount
        self.model.layoutChanged.emit()
        self.model.calculate_total()

    def open_payment_dialog(self):
        if len(self.model._data) > 0:
            amount = self.model.total
            discounts = self.model.discounts
            productsamount = []
            for row in self.model._data:
                id = row[0]
                if id in discounts:
                    full_product_name = row[2] + " " + row[1] + " (DESCUENTO)"
                    full_product_name.strip()
                else:
                    full_product_name = row[2] + " " + row[1]
                    full_product_name = full_product_name.strip()
                product_amount = row[4]
                if type(product_amount) == float:
                    product_amount = f"{product_amount} gr."
                productamount_str = "{} x {}".format(product_amount,full_product_name)
                productsamount.append(productamount_str)
            dlg = RegisterPaymentDialog(productsamount=productsamount,amount=amount)
            dlg.data.connect(self.save_payment)
            dlg.exec()
    
    def save_payment(self, payment_data):
        products = self.model._data
        discounts = self.model.discounts
        deals_0 = self.model.deals_0
        deals_1 = self.model.deals_1
        successful_payment = save_payment(payment_data, products)
        couldnt_update = substract_from_stock(products, deals_0, deals_1)
        succesful_discount_update = update_discount(products, discounts)
        succesful_deal_update = update_deal(products, deals_0 + deals_1)
        messages = []
        if successful_payment:
            self.model.reset_basket()
            self.model.layoutChanged.emit()
            self.table.clearSelection()
            self.payment_saved.emit()
            messages.append("Pago registrado correctamente.")
            if not couldnt_update:
                messages.append("Inventario actualizado exitosamente.")
            else:
                if isinstance(couldnt_update, list):
                    messages.append("Revisar inventario de: \n {}".format("\n".join(couldnt_update)))
                else:
                    messages.append("Error al actualizar inventario.")
            if discounts:
                if succesful_discount_update:
                    messages.append("Canje de descuento actualizado exitosamente.")
                else:
                    messages.append("Error al actualizar canjes de descuento.")
            if deals_0 or deals_1:
                if succesful_deal_update:
                    messages.append("Canje de promoción actualizado exitosamente.")
                else:
                    messages.append("Error al actualizar canjes de promoción.")
            QMessageBox.information(self,"Pago exitoso","\n".join(messages))
            self.model
        else:
            QMessageBox.critical(self, "Registro fallido", "Ha ocurrido un error. Contacte al administrador.")
