from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QFormLayout,
    QLabel,
    QComboBox,
    QTextEdit,
    QDialogButtonBox
)

from PySide6.QtCore import Signal

class RegisterPaymentDialog(QDialog):
    data = Signal(dict)
    def __init__(self, productsamount=[], amount=0):
        super().__init__()

        self.amount = float(amount)

        h1 = QLabel("TOTAL: ${}".format(amount))
        h1.setStyleSheet("font-size: 20px;")

        productsamount_label = QLabel("\n".join(productsamount))

        form = QFormLayout()
        self.payment_form_input = QComboBox()
        self.payment_form_input.addItems(["-- SELECCIONAR --","Tarjeta","Efectivo","Otro"])
        self.note = QTextEdit()
        form.addRow("Forma de Pago", self.payment_form_input)
        form.addRow("Nota", self.note)

        button_box = QDialogButtonBox(QDialogButtonBox.Cancel | QDialogButtonBox.Save)
        button_box.accepted.connect(self.validate_input)
        button_box.rejected.connect(self.close)

        self.message_label = QLabel()
        self.message_label.hide()
        self.message_label.setStyleSheet("color: red;")

        layout = QVBoxLayout()
        layout.addWidget(h1)
        layout.addWidget(productsamount_label)
        layout.addLayout(form)
        layout.addWidget(self.message_label)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def validate_input(self):
        self.reset_message()
        payment_form = self.payment_form_input.currentText()
        note = self.note.toPlainText()
        if payment_form != "-- SELECCIONAR --":
            if payment_form == "Otro" and not note:
                error_message = "Agregue una nota describiendo la forma de pago"
                self.message_label.setText(error_message)
                self.message_label.show()
            else:
                payment_data = {
                    "payment_form": payment_form,
                    "note": note,
                    "amount": self.amount
                }
                self.data.emit(payment_data)
                self.close()
        else:
            error_message = "Seleccione una forma de pago."
            self.message_label.setText(error_message)
            self.message_label.show()

    def reset_message(self):
        self.message_label.hide()
        self.message_label.clear()