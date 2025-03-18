from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QSpinBox,
    QDoubleSpinBox,
    QVBoxLayout,
    QRadioButton,
    QHBoxLayout,
    QLabel,
    QMessageBox
)
from PySide6.QtCore import Signal

class SetAmountDialog(QDialog):
    int_amount = Signal(int)
    float_amount = Signal(float)
    def __init__(self, product_data):
        super().__init__()

        text_label = QLabel("Ingrese la cantindad de {} a añadir.".format(product_data["product"]))

        self.int_amount_option = QRadioButton("Unidades")
        self.float_amount_option = QRadioButton("Gramos")

        self.options_layout = QHBoxLayout()
        self.options_layout.addWidget(self.int_amount_option)
        self.options_layout.addWidget(self.float_amount_option)

        self.int_amount_input = QSpinBox()
        self.int_amount_input.setSingleStep(1)
        self.int_amount_input.setRange(0,999)
        self.int_amount_input.clear()

        self.float_amount_input = QDoubleSpinBox()
        self.float_amount_input.setSingleStep(1)
        self.float_amount_input.setRange(0,999)
        self.float_amount_input.clear()

        self.float_amount_input.hide()

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        cancel_btn = button_box.button(QDialogButtonBox.Cancel)
        cancel_btn.setText("Cancelar")

        layout = QVBoxLayout()
        layout.addWidget(text_label)
        layout.addWidget(self.int_amount_input)
        layout.addWidget(self.float_amount_input)
        layout.addLayout(self.options_layout)
        layout.addWidget(button_box)

        self.setLayout(layout)

        if product_data["category"] == "Granel":
            self.float_amount_option.setChecked(True)
            self.toggle_inputs()
            self.int_amount_option.setEnabled(False)
        else:
            self.int_amount_option.setChecked(True)
            self.float_amount_option.setEnabled(False)

        self.int_amount_option.toggled.connect(self.toggle_inputs)
        
        button_box.accepted.connect(self.validate_input)
        button_box.rejected.connect(self.close)

    def toggle_inputs(self):
        if self.int_amount_option.isChecked():
            self.int_amount_input.show()
            self.float_amount_input.hide()
            self.float_amount_input.setValue(0)
        else:
            self.float_amount_input.show()
            self.int_amount_input.hide()
            self.int_amount_input.setValue(1)

    def validate_input(self):
        if self.float_amount_option.isChecked():
            if self.float_amount_input.value():
                self.emit_amount()
                self.close()
            else:
                QMessageBox.information(self, "Cantidad", "Seleccione una cantidad.")
        else:
            if self.int_amount_input.value() > 0:
                self.emit_amount()
                self.close()
            else:
                QMessageBox.information(self, "Cantidad", "Seleccione una cantidad.")
    
    def emit_amount(self):
        if self.int_amount_option.isChecked():
            self.int_amount.emit(self.int_amount_input.value())
        else:
            self.float_amount.emit(self.float_amount_input.value())