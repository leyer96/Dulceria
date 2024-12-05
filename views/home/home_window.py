from PySide6.QtWidgets import (
    QCheckBox,
    QGridLayout,
    QPushButton,
    QWidget,
)
from views.home.search_widget import SearchWidget
from views.home.products_table import SearchBox
from views.home.basket_widget import BasketWidget

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
        self.search_widget.search_input.returnPressed.connect(self.handle_search)
        self.search_box.item_data.connect(self.checkout.model.load_item)
        
        # CONFIG
        self.menu.go_to_home_btn.hide()
        
        # LAYOUT
        grid = QGridLayout()
        grid.addWidget(self.search_widget, 0, 0, 2, 12)
        grid.addWidget(self.search_box, 2, 0, 5, 9)
        grid.addWidget(self.checkout, 7, 0, 5, 12)
        grid.addWidget(self.menu, 2, 9, 5, 3)
        self.setLayout(grid)
        
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
