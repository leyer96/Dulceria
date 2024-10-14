from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QSpinBox,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import Signal

class SetAmountDialog(QDialog):
    amount = Signal(int)
    def __init__(self, product, amount=1):
        super().__init__()

        text = QLabel("Ingrese la cantindad de {} a añadir.".format(product))

        form = QFormLayout()
        amount_input = QSpinBox()
        amount_input.setSingleStep(1)
        amount_input.setRange(1,999)
        amount_input.setValue(amount)
        form.addRow("Cantidad:", amount_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        layout = QVBoxLayout()
        layout.addWidget(text)
        layout.addLayout(layout)
        layout.addWidget(amount_input)
        layout.addWidget(button_box)

        self.setLayout(layout)

        button_box.accepted.connect(lambda: self.amount.emit(amount_input.value()))
        button_box.accepted.connect(self.close)

        button_box.rejected.connect(self.close)

        