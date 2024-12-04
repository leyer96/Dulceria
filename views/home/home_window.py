from PySide6.QtWidgets import (
    QCheckBox,
    QGridLayout,
    QPushButton,
    QWidget,
)
from views.home.search_widget import SearchWidget
from views.home.search_box import SearchBox
from views.home.basket_widget import BasketWidget
from views.home.menu_widget import Menu
from views.dialogs.add_item import AddItemDialog

class HomeWindow(QWidget):
    def __init__(self, db):
        super().__init__()

        self.db = db

        grid = QGridLayout()

        self.search_widget = SearchWidget()
        self.search_box = SearchBox(db)
        self.checkout = BasketWidget()
        self.menu = Menu()

        # SIGNALS
        self.search_widget.search_btn.clicked.connect(self.handle_search)
        self.search_widget.search_input.returnPressed.connect(self.handle_search)
        self.search_box.item_data.connect(self.checkout.model.load_item)
        self.menu.add_btn.clicked.connect(self.open_add_dialog)
        

        grid.addWidget(self.search_widget, 0, 0, 2, 12)
        grid.addWidget(self.search_box, 2, 0, 5, 8)
        grid.addWidget(self.checkout, 7, 0, 4, 12)
        grid.addWidget(self.menu, 2, 9, 5, 2)


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

    def open_add_dialog(self):
        dlg = AddItemDialog(self.db)
        dlg.exec()