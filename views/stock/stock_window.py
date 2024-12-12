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
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from views.home.search_widget import SearchWidget
from models.stock_model import StockModel
from models.batch_model import BatchModel
from views.dialogs.add_batch import AddBatchDialog
from utils import Paths, toggle_btns_state

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
        add_batch_btn = QPushButton(QIcon(Paths.icon("plus-button.png")),"Agregar Lote")
        self.resolve_batch_btn = QPushButton(QIcon(Paths.icon("blue-document-task.png")), "Resolver")
        
        # CONFIG
        self.stock_table.setModel(self.stock_model)
        self.stock_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.stock_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.stock_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.stock_model.get_all_stock()

        self.batch_table.setModel(self.batch_model)
        self.batch_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.batch_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.batch_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.batch_table.clicked.connect(self.on_clicked_row)
        self.batch_model.get_all_batchs()

        self.selected_row = -1
        self.resolve_batch_btn.setEnabled(False)
        self.menu.go_to_stock_btn.hide()
        stock_title.setStyleSheet("font-size: 30px; font-weight: bold")

         # SIGNALS
        self.search_widget.search_btn.clicked.connect(self.handle_search)
        self.search_widget.search_btn.clicked.connect(lambda: self.resolve_batch_btn.setEnabled(False))
        self.search_widget.search_input.returnPressed.connect(self.handle_search)
        self.search_widget.search_input.returnPressed.connect(lambda: self.resolve_batch_btn.setEnabled(False))
        add_batch_btn.clicked.connect(self.open_add_batch_dialog)
        self.resolve_batch_btn.clicked.connect(self.resolve_batch)
        # self.model.success.connect(self.toggle_btns_state)
        
        # LAYOUT
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(add_batch_btn)
        buttons_layout.addWidget(self.resolve_batch_btn)

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
        self.batch_model.search(str, filter)

    def on_clicked_row(self, index):
        self.selected_row = index.row()
        if self.selected_row > -1:
            if not self.resolve_batch_btn.isEnabled():
                toggle_btns_state([self.resolve_batch_btn])
    
    def open_add_batch_dialog(self):
        dlg = AddBatchDialog()
        dlg.saved.connect(lambda: self.resolve_batch_btn.setEnabled(False))
        dlg.saved.connect(self.stock_model.refresh_table)
        dlg.saved.connect(self.batch_model.refresh_table)
        dlg.exec()

    def resolve_batch(self):
        row = self.selected_row
        if row > -1:
            batch_id = self.batch_model.data(self.batch_model.index(row, 0), Qt.DisplayRole)
            self.batch_model.update_batch_show_status(batch_id)