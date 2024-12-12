from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget
    )
from PySide6.QtGui import QIcon
from utils import Paths, default_cb_str


class SearchWidget(QWidget):
    def __init__(self):
        super().__init__()
        # SEARCH INPUT SECTION
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar Producto")
        self.search_btn = QPushButton()
        search_btn_icon = QIcon(Paths.icon("application-search-result.png"))
        self.search_btn.setIcon(search_btn_icon)
        self.search_checkbox = QCheckBox("Consultar")

        search_input_layout = QHBoxLayout()
        search_input_layout.addWidget(self.search_input)
        search_input_layout.addWidget(self.search_btn)
        search_input_layout.addWidget(self.search_checkbox)
        # FILTER BY SECTION
        filter_label = QLabel("Filtrar por:")
        self.filter_by_name = QRadioButton("Nombre")
        self.filter_by_name.setChecked(True)
        self.filter_by_category = QRadioButton("Categoría")
        self.filter_by_code = QRadioButton("Código")

        filter_section_layout = QHBoxLayout()
        filter_section_layout.addWidget(filter_label)
        filter_section_layout.addWidget(self.filter_by_name)
        filter_section_layout.addWidget(self.filter_by_category)
        filter_section_layout.addWidget(self.filter_by_code)
        # LAYOUT
        layout = QVBoxLayout()
        layout.addLayout(search_input_layout)
        layout.addLayout(filter_section_layout)
        self.setLayout(layout)