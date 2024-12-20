from PySide6.QtWidgets import (
    QTableView,
    QGridLayout,
    QAbstractItemView,
    QHeaderView,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from views.home.search_widget import SearchWidget
from models.stock_model import StockModel
from models.batch_model import BatchModel
from views.dialogs.add_batch import AddBatchDialog
from views.dialogs.edit_stock import EditStockDialog
from utils import Paths, toggle_btns_state, load_settings
from datetime import datetime

class StockWindow(QWidget):
    def __init__(self, db, menu):
        super().__init__()

        self.db = db
        self.menu = menu
        self.search_widget = SearchWidget()
        self.stock_table = QTableView()
        self.batch_table = QTableView()
        self.stock_model = StockModel(db)
        self.batch_model = BatchModel(db)
        stock_title = QLabel("Stock")
        batch_title = QLabel("Lotes")
        self.edit_stock_btn = QPushButton(QIcon(Paths.icon("pencil.png")), "Editar Stock")
        self.add_batch_btn = QPushButton(QIcon(Paths.icon("plus-button.png")),"Agregar Lote")
        self.resolve_batch_btn = QPushButton(QIcon(Paths.icon("blue-document-task.png")), "Resolver")
        
        # CONFIG
        self.stock_table.setModel(self.stock_model)
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stock_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.stock_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.stock_table.clicked.connect(self.on_clicked_stock_row)

        self.batch_table.setModel(self.batch_model)
        self.batch_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.batch_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.batch_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.batch_table.clicked.connect(self.on_clicked_batch_row)

        self.selected_batch_row = -1
        self.selected_stock_row = -1
        self.resolve_batch_btn.setEnabled(False)
        self.edit_stock_btn.setEnabled(False)
        self.menu.go_to_stock_btn.setEnabled(False)

        
        stock_title.setStyleSheet("font-size: 30px; font-weight: bold")

         # SIGNALS
        self.search_widget.search_btn.clicked.connect(self.handle_search)
        self.search_widget.search_input.returnPressed.connect(self.handle_search)
        self.search_widget.search_input.returnPressed.connect(lambda: self.resolve_batch_btn.setEnabled(False))
        self.edit_stock_btn.clicked.connect(self.open_edit_stock_dialog)
        self.add_batch_btn.clicked.connect(self.open_add_batch_dialog)
        self.resolve_batch_btn.clicked.connect(self.resolve_batch)
        
        # LAYOUT
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_batch_btn)
        buttons_layout.addWidget(self.resolve_batch_btn)

        grid = QGridLayout()
        grid.addWidget(stock_title, 0, 0, 1, 12)
        grid.addWidget(self.search_widget, 1, 0, 1, 9)
        grid.addWidget(self.stock_table, 2, 0, 4, 9)
        grid.addWidget(self.edit_stock_btn, 6, 0, 1, 2)
        grid.addWidget(batch_title, 6, 4, 1, 2)
        grid.addWidget(self.batch_table, 7, 0, 4, 9)
        grid.addLayout(buttons_layout, 11, 0, 1, 9)
        grid.addWidget(self.menu, 2, 9, 5, 3)
        
        self.setLayout(grid)

        self.load_settings()
        
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
        self.batch_model.search(str, filter)
        self.resolve_batch_btn.setEnabled(False)
        self.edit_stock_btn.setEnabled(False)
        if self.search_widget.filter_by_code.isChecked():
            self.search_widget.search_input.setText("")

    def on_clicked_batch_row(self, index):
        self.selected_batch_row = index.row()
        if self.selected_batch_row > -1:
            if not self.resolve_batch_btn.isEnabled():
                toggle_btns_state([self.resolve_batch_btn])

    def on_clicked_stock_row(self, index):
        self.selected_stock_row = index.row()
        if self.selected_stock_row > -1:
            if not self.edit_stock_btn.isEnabled():
                toggle_btns_state([self.edit_stock_btn])

    def open_edit_stock_dialog(self):
        row = self.selected_stock_row
        if row != -1:
            product_id = self.stock_model.data(self.stock_model.index(row, 0), Qt.DisplayRole)
            product = self.stock_model.data(self.stock_model.index(row, 1), Qt.DisplayRole)
            brand = self.stock_model.data(self.stock_model.index(row, 2), Qt.DisplayRole)
            amount = self.stock_model.data(self.stock_model.index(row, 4), Qt.DisplayRole)
            product_data = {
                "product_id": product_id,
                "product": product,
                "brand": brand,
                "amount": amount
            }
            dlg = EditStockDialog(product_data)
            dlg.saved.connect(lambda: self.resolve_batch_btn.setEnabled(False))
            dlg.saved.connect(lambda: self.edit_stock_btn.setEnabled(False))
            dlg.saved.connect(self.stock_model.refresh_table)
            dlg.saved.connect(self.batch_model.refresh_table)
            dlg.exec()  
    
    def open_add_batch_dialog(self):
        dlg = AddBatchDialog()
        dlg.saved.connect(lambda: self.resolve_batch_btn.setEnabled(False))
        dlg.saved.connect(lambda: self.edit_stock_btn.setEnabled(False))
        dlg.saved.connect(self.stock_model.refresh_table)
        dlg.saved.connect(self.batch_model.refresh_table)
        dlg.exec()

    def resolve_batch(self):
        row = self.selected_batch_row
        if row > -1:
            batch_id = self.batch_model.data(self.batch_model.index(row, 0), Qt.DisplayRole)
            self.batch_model.update_batch_show_status(batch_id)

    def load_settings(self):
        settings = load_settings()
        if not settings["permissions"]["stock_window"]["edit"]:
            self.edit_stock_btn.hide()
        else:
            self.edit_stock_btn.show()
        if not settings["permissions"]["stock_window"]["add"]:
            self.add_batch_btn.hide()
        else:
            self.add_batch_btn.show()
        if not settings["permissions"]["stock_window"]["resolve"]:
            self.resolve_batch_btn.hide()
        else:
            self.resolve_batch_btn.show()