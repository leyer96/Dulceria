from PySide6.QtWidgets import (
    QTableView,
    QGridLayout,
    QAbstractItemView,
    QHeaderView,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QMessageBox
)
from PySide6.QtGui import QIcon
from views.home.search_widget import SearchWidget
from models.search_model import SearchModel
from views.dialogs.add_item import AddItemDialog
from views.dialogs.edit_item import EditItemDialog
from utils import Paths

class ProductsWindow(QWidget):
    def __init__(self, db, menu):
        super().__init__()

        self.db = db
        self.menu = menu
        self.search_widget = SearchWidget()
        self.add_product_btn = QPushButton(QIcon(Paths.icon("plus-button.png")),"Agregar Producto")
        self.edit_product_btn = QPushButton(QIcon(Paths.icon("pencil.png")),"Editar Producto")
        self.delete_product_btn = QPushButton(QIcon(Paths.icon("minus-button.png")),"Eliminar Producto")
        self.table = QTableView()
        self.model = SearchModel(db)

        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        
        # CONFIG
        self.edit_product_btn.setEnabled(False)
        self.delete_product_btn.setEnabled(False)
        self.menu.go_to_products_btn.hide()
        self.selected_row = -1

         # SIGNALS
        self.search_widget.search_btn.clicked.connect(self.handle_search)
        self.search_widget.search_input.returnPressed.connect(self.handle_search)
        self.table.clicked.connect(self.on_clicked_row)
        self.add_product_btn.clicked.connect(self.open_add_dialog)
        self.edit_product_btn.clicked.connect(lambda: self.open_edit_dialog(self.selected_row))
        self.delete_product_btn.clicked.connect(lambda: self.delete_product(self.selected_row))
        self.model.success.connect(self.toggle_btns_state)
        
        # LAYOUT
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_product_btn)
        buttons_layout.addWidget(self.edit_product_btn)
        buttons_layout.addWidget(self.delete_product_btn)

        grid = QGridLayout()
        grid.addWidget(self.search_widget, 0, 0, 2, 12)
        grid.addLayout(buttons_layout, 2, 0, 1, 9)
        grid.addWidget(self.table, 3, 0, 9, 9)
        grid.addWidget(self.menu, 2, 9, 5, 3)
        self.setLayout(grid)
        
    def handle_search(self):
        str = self.search_widget.search_input.text()
        self.search_str = str
        filter = ""
        if self.search_widget.filter_by_name.isChecked():
            filter = "name"
        elif self.search_widget.filter_by_category.isChecked():
            filter = "category"
        elif self.search_widget.filter_by_code.isChecked():
            filter = "code"
        else:
            pass
        self.filter = filter
        self.model.search(str, filter)

    def on_clicked_row(self, index):
        self.selected_row = index.row()
        if self.selected_row > -1:
            if not self.edit_product_btn.isEnabled():
                self.toggle_btns_state()
    
    def open_add_dialog(self):
        dlg = AddItemDialog(self.db)
        dlg.saved.connect(self.model.refresh_table)
        dlg.saved.connect(self.toggle_btns_state)
        dlg.exec()
    
    def open_edit_dialog(self, row):
        if row != None:
            product_id = self.model.data(self.model.index(row, 0))
            dlg = EditItemDialog(self.db, product_id)
            dlg.item_edited.connect(self.model.refresh_table)
            dlg.item_edited.connect(self.toggle_btns_state)
            dlg.exec()
        
    def delete_product(self, row):
        if row != None:
            accepted = QMessageBox.question(self, "Confirmar", "Estás seguro que quieres eliminar este producto?")
            if accepted:
                product_id = int(self.model.data(self.model.index(row, 0)))
                self.model.delete_product(product_id)

    def toggle_btns_state(self):
        if self.edit_product_btn.isEnabled():
            self.edit_product_btn.setEnabled(False)
            self.delete_product_btn.setEnabled(False)
        else:
            self.edit_product_btn.setEnabled(True)
            self.delete_product_btn.setEnabled(True)
