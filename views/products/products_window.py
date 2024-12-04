from PySide6.QtWidgets import (
    QTableView,
    QGridLayout,
    QAbstractItemView,
    QLineEdit,
    QHeaderView,
    QPushButton,
    QVBoxLayout,
    QWidget
)
from views.home.search_widget import SearchWidget
from views.home.menu_widget import Menu
from models.search_model import SearchModel

class ProductsWindow(QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.search_widget = SearchWidget()
        self.menu = Menu()
        self.table = QTableView()
        self.model = SearchModel(db)
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.search_widget.search_btn.clicked.connect(self.handle_search)
        self.search_widget.search_input.returnPressed.connect(self.handle_search)
        # PASAR METODOS A WIDGET MENU
        # self.menu.go_to_add_product_btn.clicked.connect(self.open_add_dialog)

        layout = QVBoxLayout()
        layout.addWidget(self.search_widget)
        layout.addWidget(self.search_widget)

        grid = QGridLayout()

        grid.addWidget(self.search_widget, 0, 0, 2, 12)
        grid.addWidget(self.table, 2, 0, 5, 10)
        grid.addWidget(self.menu, 2, 11, 5, 1)

        self.menu.go_to_product_list_btn.hide()

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
        self.model.search(str, filter)