from PySide6.QtWidgets import (
    QDialog,
    QComboBox,
    QPushButton,
    QDialogButtonBox,
    QHBoxLayout,
    QVBoxLayout,
    QRadioButton,
    QLabel
)
from PySide6.QtCore import Signal
from datetime import datetime

today = datetime.today()
curr_month = today.month

from utils import months

available_months = months[0:curr_month]

class SelectExportDataDialog(QDialog):
    option_selected = Signal(str)
    def __init__(self, is_query):
        super().__init__()
        l1 = QLabel("Exportar datos")
        self.current_query_option = QRadioButton("Selección Actual")
        self.month_option = QRadioButton("Mes")
        self.month_input = QComboBox()
        self.month_input.addItems(["--SELECCIONAR--", *available_months])
        self.all_option = QRadioButton("Todo")
        self.msg_label = QLabel()

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        cancel_btn = self.button_box.button(QDialogButtonBox.Cancel)
        cancel_btn.setText("Cancelar")

        save_btn = self.button_box.button(QDialogButtonBox.Ok)
        save_btn.setText("Exportar")

        # CONFIG
        if not is_query:
            self.current_query_option.setEnabled(False)
            self.month_option.setChecked(True)
        else:
            self.current_query_option.setChecked(True)
        self.msg_label.hide()
        self.msg_label.setStyleSheet("color: red;")
        
        # SIGNALS
        self.button_box.accepted.connect(self.emit_export_option)
        self.button_box.rejected.connect(self.close)
        self.month_input.currentIndexChanged.connect(lambda: self.month_option.setChecked(True))
        self.month_input.currentIndexChanged.connect(self.msg_label.hide)
        
        month_input_layout = QHBoxLayout()
        month_input_layout.addWidget(self.month_option)
        month_input_layout.addWidget(self.month_input)
        
        layout = QVBoxLayout()
        layout.addWidget(l1)
        layout.addWidget(self.current_query_option)
        layout.addLayout(month_input_layout)
        layout.addWidget(self.all_option)
        layout.addWidget(self.msg_label)
        layout.addWidget(self.button_box)

        self.setLayout(layout)
    
    def emit_export_option(self):
        self.msg_label.hide()
        if self.current_query_option.isChecked():
            self.option_selected.emit("curr")
            self.close()
        elif self.month_option.isChecked():
            month = self.month_input.currentText()
            if month != "--SELECCIONAR--":
                self.option_selected.emit(self.month_input.currentText())
                self.close()
            else:
                self.msg_label.setText("Seleccione un mes")
                self.msg_label.show()
        else:
            self.option_selected.emit("all")
            self.close()
