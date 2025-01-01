from PySide6.QtWidgets import (
    QTableView,
    QGridLayout,
    QAbstractItemView,
    QHeaderView,
    QPushButton,
    QWidget,
    QMessageBox,
    QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from views.home.search_widget import SearchWidget
from models.discount_model import DiscountModel
from models.deal_model import DealModel
from utils import Paths, load_settings
import sqlite3

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
        self.delete_deal_btn.clicked.connect(self.delete_deal)
        self.delete_discount_btn.clicked.connect(self.delete_discount)

        grid = QGridLayout()
        grid.addWidget(deals_title, 0, 0, 1, 12)
        grid.addWidget(self.search_widget, 1, 0, 1, 9)
        grid.addWidget(self.deal_table, 2, 0, 4, 9)
        grid.addWidget(self.delete_deal_btn, 6, 0, 1, 2)
        grid.addWidget(discounts_title, 6, 4, 1, 2)
        grid.addWidget(self.discount_table, 7, 0, 4, 9)
        grid.addWidget(self.delete_discount_btn, 11, 0, 1, 9)
        grid.addWidget(self.menu, 2, 9, 5, 3)
        
        for i in range(12):
            grid.setColumnStretch(i, 1)
        for j in range(12):
            grid.setRowStretch(j, 1)
        
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

    def delete_deal(self):
        deal_id = self.deal_model.data(self.deal_model.index(self.selected_deal_row, 0), Qt.DisplayRole)
        deal = self.deal_model.data(self.deal_model.index(self.selected_deal_row, 2), Qt.DisplayRole)
        product = self.deal_model.data(self.deal_model.index(self.selected_deal_row, 1), Qt.DisplayRole)
        answer = QMessageBox.question(self, "Eliminar Promoción", f"¿Eliminar promoción: {deal} para {product}?")
        if answer == QMessageBox.Yes:
            con = sqlite3.connect(Paths.test("db.db"))
            # con = sqlite3.connect(Paths.db())
            cur = con.cursor()
            try:
                cur.execute("DELETE FROM deal WHERE id = ?", (deal_id,))
            except sqlite3.Error as e:
                print(e)
                QMessageBox.alert(self, "Error", "Ha ocurrido un error. Contacte al administrador.")
            else:
                con.commit()
                self.deal_model.refresh_table()

    def delete_discount(self):
        discount_id = self.discount_model.data(self.discount_model.index(self.selected_discount_row, 0), Qt.DisplayRole)
        product = self.discount_model.data(self.discount_model.index(self.selected_discount_row, 1), Qt.DisplayRole)
        answer = QMessageBox.question(self, "Eliminar Promoción", f"¿Eliminar descuento para {product}?")
        if answer == QMessageBox.Yes:
            con = sqlite3.connect(Paths.test("db.db"))
            # con = sqlite3.connect(Paths.db())
            cur = con.cursor()
            try:
                cur.execute("DELETE FROM discount WHERE id = ?", (discount_id,))
            except sqlite3.Error as e:
                print(e)
                QMessageBox.alert(self, "Error", "Ha ocurrido un error. Contacte al administrador.")
            else:
                con.commit()
                self.discount_model.refresh_table()

    def load_settings(self):
        settings = load_settings()
        if not settings["permissions"]["deals_window"]["delete_discount"]:
            self.delete_discount_btn.hide()
        else:
            self.delete_discount_btn.show()
        if not settings["permissions"]["deals_window"]["delete_deal"]:
            self.delete_deal_btn.hide()
        else:
            self.delete_deal_btn.show()