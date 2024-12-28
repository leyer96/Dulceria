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
from models.discount_model import DiscountModel
from models.deal_model import DealModel
from utils import Paths, load_settings

class DealsWindow(QWidget):
    def __init__(self, db, menu):
        super().__init__()

        self.db = db
        self.menu = menu
        self.search_widget = SearchWidget()
        self.deal_table = QTableView()
        self.discount_table = QTableView()
        self.deal_model = DealModel(db)
        self.discount_model = DiscountModel(db)
        deals_title = QLabel("Promociones")
        discounts_title = QLabel("Descuentos")
        self.delete_deal_btn = QPushButton(QIcon(Paths.icon("minus-button.png")), "Eliminar")
        self.delete_discount_btn = QPushButton(QIcon(Paths.icon("minus-button.png")), "Eliminar")
        
        # CONFIG
        self.deal_table.setModel(self.deal_model)
        self.deal_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.deal_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.deal_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.deal_table.clicked.connect(self.on_clicked_deal_row)

        self.discount_table.setModel(self.discount_model)
        self.discount_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.discount_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.discount_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.discount_table.clicked.connect(self.on_clicked_discount_row)

        self.selected_deal_row = -1
        self.selected_discount_row = -1
        self.delete_deal_btn.setEnabled(False)
        self.delete_discount_btn.setEnabled(False)
        self.menu.go_to_deals_btn.setEnabled(False)

        
        deals_title.setStyleSheet("font-size: 30px; font-weight: bold")

         # SIGNALS
        self.search_widget.search_btn.clicked.connect(self.handle_search)
        self.search_widget.search_input.returnPressed.connect(self.handle_search)
        self.deal_model.success.connect(self.hide_deal_columns)
        self.deal_model.error.connect(self.hide_deal_columns)
        self.deal_model.success.connect(lambda: self.delete_deal_btn.setEnabled(False))
        self.deal_model.error.connect(lambda: self.delete_deal_btn.setEnabled(False))
        self.discount_model.success.connect(lambda: self.delete_discount_btn.setEnabled(False))
        self.discount_model.error.connect(lambda: self.delete_discount_btn.setEnabled(False))
        
        # LAYOUT
        # buttons_layout = QHBoxLayout()
        # buttons_layout.addWidget(btn)
        # buttons_layout.addWidget(btn)
        # buttons_layout.addWidget(btn)

        grid = QGridLayout()
        grid.addWidget(deals_title, 0, 0, 1, 12)
        grid.addWidget(self.search_widget, 1, 0, 1, 9)
        grid.addWidget(self.deal_table, 2, 0, 4, 9)
        grid.addWidget(self.delete_deal_btn, 6, 0, 1, 2)
        grid.addWidget(discounts_title, 6, 4, 1, 2)
        grid.addWidget(self.discount_table, 7, 0, 4, 9)
        grid.addWidget(self.delete_discount_btn, 11, 0, 1, 9)
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
        self.deal_model.search(str, filter)
        self.discount_model.search(str, filter)
        if self.search_widget.filter_by_code.isChecked():
            self.search_widget.search_input.setText("")

    def hide_deal_columns(self):
        for i in range(5, 9):
            self.deal_table.hideColumn(i)

    def on_clicked_deal_row(self, index):
        self.selected_deal_row = index.row()
        if self.selected_deal_row > -1:
            if not self.delete_deal_btn.isEnabled():
                self.delete_deal_btn.setEnabled(True)

    def on_clicked_discount_row(self, index):
        self.selected_discount_row = index.row()
        if self.selected_discount_row > -1:
            if not self.delete_discount_btn.isEnabled():
                self.delete_discount_btn.setEnabled(True)

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

    def open_discount_dialog(self):
        row = self.selected_batch_row
        if row != -1:
            batch_id = self.batch_model.data(self.batch_model.index(row, 0), Qt.DisplayRole)
            dlg = AddDiscountDialog(batch_id)
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
        # if not settings["permissions"]["stock_window"]["edit"]:
        #     self.edit_stock_btn.hide()
        # else:
        #     self.edit_stock_btn.show()
        # if not settings["permissions"]["stock_window"]["add"]:
        #     self.add_batch_btn.hide()
        # else:
        #     self.add_batch_btn.show()
        # if not settings["permissions"]["stock_window"]["resolve"]:
        #     self.resolve_batch_btn.hide()
        # else:
        #     self.resolve_batch_btn.show()