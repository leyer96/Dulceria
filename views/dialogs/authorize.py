from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLineEdit,
    QVBoxLayout,
    QLabel
)
from PySide6.QtCore import Signal
from utils import load_settings

class AuthorizeDialog(QDialog):
    authorized = Signal()
    def __init__(self):
        super().__init__()

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        
        form = QFormLayout()
        form.addRow("Contraseña", self.password_input)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        cancel_btn = button_box.button(QDialogButtonBox.Cancel)
        cancel_btn.setText("Cancelar")

        button_box.rejected.connect(self.close)
        button_box.accepted.connect(self.authorize)
        
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Ingrese contraseña de desarrollador"))
        layout.addLayout(form)
        layout.addWidget(button_box)

        self.setLayout(layout)

        self.load_settings()

    def load_settings(self):
        settings = load_settings()
        self.password = settings["developer"]["password"]
    
    def authorize(self):
        password = self.password_input.text()
        if password == self.password:
            self.authorized.emit()
            self.close()

        