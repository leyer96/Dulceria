from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout
)
from PySide6.QtCore import Qt
from views.home.search_widget import SearchWidget
from views.home.products_table import SearchBox
from views.home.basket_widget import BasketWidget
from utils import load_settings

class HomeWindow(QWidget):
    def __init__(self, db, menu):
        super().__init__()

        self.db = db
        self.menu = menu
        self.search_widget = SearchWidget()
        self.search_box = SearchBox(db)
        self.checkout = BasketWidget()

        # SIGNALS
        self.search_widget.search_btn.clicked.connect(self.handle_search)
        self.search_widget.search_btn.clicked.connect(lambda: self.search_box.add_btn.setEnabled(False))
        self.search_widget.search_input.returnPressed.connect(self.handle_search)
        self.search_widget.search_input.returnPressed.connect(lambda: self.search_box.add_btn.setEnabled(False))
        self.search_box.item_data.connect(self.checkout.model.load_item)
        
        # CONFIG
        self.menu.go_to_home_btn.setEnabled(False)
        
        # LAYOUT
        layout = QVBoxLayout()

        sublayout = QHBoxLayout()
        sublayout_left = QVBoxLayout()
        sublayout_left.addWidget(self.search_widget)
        sublayout_left.addWidget(self.search_box)
        sublayout.addLayout(sublayout_left)
        
        sublayout_right = QVBoxLayout()
        sublayout_right.addWidget(self.menu)
        sublayout_right.insertSpacing(0, 200)
        sublayout_right.setAlignment(self.menu, Qt.AlignTop)

        sublayout.addLayout(sublayout_left)
        sublayout.addLayout(sublayout_right)

        sublayout.setStretch(0, 4)
        sublayout.setStretch(1, 1)

        layout.addLayout(sublayout)
        layout.addWidget(self.checkout)

        self.setLayout(layout)
        self.load_settings()
        
    def handle_search(self):
        str = self.search_widget.search_input.text()
        filter = ""
        if self.search_widget.filter_by_name.isChecked():
            filter = "name"
        elif self.search_widget.filter_by_category.isChecked():
            filter = "category"
        elif self.search_widget.filter_by_code.isChecked():
            filter = "code"
        else:
            pass
        self.search_box.model.search(str, filter)
        if self.search_widget.filter_by_code.isChecked():
            self.search_widget.search_input.setText("")
    
    def load_settings(self):
        settings = load_settings()
        if not settings["permissions"]["payments_window"]["view"]:
            self.menu.go_to_payments_btn.hide()
        else:
            self.menu.go_to_payments_btn.show()