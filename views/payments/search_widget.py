from PySide6.QtWidgets import (
    QCalendarWidget,
    QCheckBox,
    QDateEdit,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
    )
from PySide6.QtCore import QDate, Qt, Signal, QLocale
from PySide6.QtGui import QIcon
from utils import Paths


class SearchWidget(QWidget):
    data = Signal(dict)
    def __init__(self):
        super().__init__()
        # SEARCH INPUT SECTION
        # SINGLE DATE
        current_date = QDate().currentDate()
        l1 = QLabel("Búsqueda por fecha:")
        self.start_date_input = QDateEdit(date=current_date, maximumDate=current_date, calendarPopup=True)
        l2 = QLabel("a")
        self.end_date_input = QDateEdit(date=current_date, maximumDate=current_date, calendarPopup=True)
        self.search_btn = QPushButton(QIcon(Paths.icon("application-search-result.png")), "")

        # SIGNALS
        self.end_date_input.dateChanged.connect(lambda date: self.start_date_input.setMaximumDate(date))
        self.search_btn.clicked.connect(self.emit_date_data)

        # CONFIG
        self.start_date_input.calendarWidget().setLocale(QLocale.Spanish)
        self.end_date_input.calendarWidget().setLocale(QLocale.Spanish)
        l1.setAlignment(Qt.AlignCenter)
        l2.setAlignment(Qt.AlignCenter)
        self.search_btn.setSizePolicy(QSizePolicy.Maximum,QSizePolicy.Maximum)

        # LAYOUT
        date_input_layout = QHBoxLayout()
        date_input_layout.addWidget(l1)
        date_input_layout.addWidget(self.start_date_input)
        date_input_layout.addWidget(l2)
        date_input_layout.addWidget(self.end_date_input)
        date_input_layout.addWidget(self.search_btn)

        layout = QVBoxLayout()
        layout.addLayout(date_input_layout)
        self.setLayout(layout)

    def emit_date_data(self):
        start_date = self.start_date_input.date()
        end_date = self.end_date_input.date()
        data = {
            "start_date": start_date,
            "end_date": end_date
        }
        self.data.emit(data)
