from PySide6.QtWidgets import (
    QTableView,
    QGridLayout,
    QAbstractItemView,
    QHeaderView,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QMessageBox,
    QLabel
)
from PySide6.QtGui import QIcon
from views.home.search_widget import SearchWidget
from models.stock_model import StockModel
from views.dialogs.edit_item import EditItemDialog
from utils import Paths

class StockWindow(QWidget):
    def __init__(self, db, menu):
        super().__init__()

        self.db = db
        self.menu = menu
        self.search_widget = SearchWidget()
        self.stock_table = QTableView()
        self.batch_table = QTableView()
        self.stock_model = StockModel(db)
        # self.batch_model = SearchModel(db)
        stock_title = QLabel("Stock")
        batch_title = QLabel("Lotes")
        add_batch_btn = QPushButton(QIcon(Paths.icon("plus-button.png")),"Agregar Lote")
        
        # CONFIG
        self.stock_table.setModel(self.stock_model)
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stock_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.stock_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.batch_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.batch_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.batch_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.menu.go_to_stock_btn.hide()
        stock_title.setStyleSheet("font-size: 30px; font-weight: bold")

         # SIGNALS
        self.search_widget.search_btn.clicked.connect(self.handle_search)
        self.search_widget.search_input.returnPressed.connect(self.handle_search)
        add_batch_btn.clicked.connect(self.open_add_batch_dialog)
        # self.model.success.connect(self.toggle_btns_state)
        
        # LAYOUT
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(add_batch_btn)

        grid = QGridLayout()
        grid.addWidget(stock_title, 0, 0, 1, 12)
        grid.addWidget(self.search_widget, 1, 0, 1, 9)
        grid.addWidget(self.stock_table, 2, 0, 4, 9)
        grid.addWidget(batch_title, 6, 0, 1, 9)
        grid.addWidget(self.batch_table, 7, 0, 4, 9)
        grid.addLayout(buttons_layout, 11, 0, 1, 9)
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
        self.stock_model.search(str, filter)

    def on_clicked_row(self, index):
        self.selected_row = index.row()
        if self.selected_row > -1:
            if not self.edit_product_btn.isEnabled():
                self.toggle_btns_state()
    
    def open_add_batch_dialog(self):
        pass
    
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
