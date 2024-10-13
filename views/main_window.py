from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QMainWindow,
    QPushButton,
    QRadioButton,
    QWidget
)
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtCore import Signal
from views.search_box import SearchBox
from views.basket_widget import BasketWidget
from views.dialogs.add_item import AddItemDialog
from utils import Paths

class MainWindow(QMainWindow):
    send_search_data = Signal(list)
    def __init__(self, db):
        super().__init__()

        self.db = db

        grid = QGridLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Buscar Producto")

        search_btn = QPushButton()
        search_btn_icon = QIcon(Paths.icon("application-search-result.png"))
        search_btn.setIcon(search_btn_icon)

        self.filter_section = QWidget()
        self.filter_label = QLabel("Filtrar por:")
        self.filter_by_name = QRadioButton("Nombre")
        self.filter_by_name.setChecked(True)
        self.filter_by_category = QRadioButton("Categoría")
        self.filter_by_code = QRadioButton("Código")
        self.filter_section_layout = QHBoxLayout()
        self.filter_section_layout.addWidget(self.filter_label)
        self.filter_section_layout.addWidget(self.filter_by_name)
        self.filter_section_layout.addWidget(self.filter_by_category)
        self.filter_section_layout.addWidget(self.filter_by_code)
        self.filter_section.setLayout(self.filter_section_layout)

        search_box = SearchBox(db)
        checkout = BasketWidget()
        search_checkbox = QCheckBox("Consultar")
        add_btn = QPushButton("Agregar Nuevo Producto")
        go_to_list_btn = QPushButton("Productos")

        # SIGNALS
        search_btn.clicked.connect(self.handle_search)
        self.search.returnPressed.connect(self.handle_search)
        self.send_search_data.connect(search_box.search)
        search_box.item_data.connect(checkout.model.load_item)
        add_btn.clicked.connect(self.open_add_dialog)
        

        grid.addWidget(self.search, 0, 0, 1, 8)
        grid.addWidget(search_btn, 0, 8, 1, 2)
        grid.addWidget(self.filter_section, 1, 0, 1, 8)
        grid.addWidget(search_box, 2, 0, 5, 8)
        grid.addWidget(checkout, 7, 0, 4, 12)
        grid.addWidget(search_checkbox, 0, 10, 1, 2)
        grid.addWidget(add_btn, 2, 9, 2, 2)
        grid.addWidget(go_to_list_btn, 5, 9, 2, 2)

        container = QWidget()
        container.setLayout(grid)

        screen = QApplication.primaryScreen()
        screen_size = screen.size()
        
        # self.resize(screen_size.width(), screen_size.height())
        self.resize(700, 500)
        
        self.setCentralWidget(container)

        self.show()

    def handle_search(self):
        str = self.search.text()
        filter = ""
        if self.filter_by_name.isChecked():
            filter = "name"
        elif self.filter_by_category.isChecked():
            filter = "category"
        elif self.filter_by_code.isChecked():
            filter = "code"
        else:
            pass
        self.send_search_data.emit([str, filter])

    def open_add_dialog(self):
        dlg = AddItemDialog(self.db)
        dlg.exec()