from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QDialogButtonBox
)
from PySide6.QtCore import Signal

class QuestionDialog(QDialog):
    accepted = Signal()
    def __init__(self, question):
        super().__init__()
        question_label = QLabel(question)
        button_box = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)

        yes_btn = button_box.button(QDialogButtonBox.Yes)
        yes_btn.setText("Sí")

        no_btn = button_box.button(QDialogButtonBox.No)

        layout = QVBoxLayout()
        layout.addWidget(question_label)
        layout.addWidget(button_box)

        no_btn.clicked.connect(self.close)
        yes_btn.clicked.connect(self.handle_accept)

        self.setLayout(layout)

    def handle_accept(self):
        self.accepted.emit()
        self.close()

