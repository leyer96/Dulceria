from PySide6.QtWidgets import (
    QTableView,
    QGridLayout,
    QAbstractItemView,
    QHeaderView,
    QPushButton,
    QWidget,
    QMessageBox,
    QLabel,
    QVBoxLayout,
    QHBoxLayout
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
        self.deals_title = QLabel("Promociones")
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

        
        self.deals_title.setStyleSheet("font-size: 30px; font-weight: bold")

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

        
        # LAYOUT
        layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(self.deals_title)
        left_layout.addWidget(self.search_widget)
        left_layout.addWidget(self.deal_table)
        left_layout.addWidget(self.delete_deal_btn)
        left_layout.addWidget(discounts_title)
        left_layout.addWidget(self.discount_table)
        left_layout.addWidget(self.delete_discount_btn)

        right_layout = QVBoxLayout()
        right_layout.addWidget(self.menu)
        right_layout.insertSpacing(0, 200)
        right_layout.setAlignment(self.menu, Qt.AlignTop)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        layout.setStretch(0, 4)
        layout.setStretch(1, 1)
        
        self.setLayout(layout)

        self.deal_model.refresh_table()
        self.discount_model.refresh_table()

        # self.get_n_deals()
        self.load_settings()
        
    def get_n_deals(self):
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        n_deals = len(cur.execute("SELECT * FROM deal").fetchall())
        n_discounts = len(cur.execute("SELECT * FROM discount").fetchall())
        total = n_deals + n_discounts
        self.deals_title.setText(f"Promociones ({total} activas)")
    
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
        if not settings["permissions"]["payments_window"]["view"]:
            self.menu.go_to_payments_btn.hide()
        else:
            self.menu.go_to_payments_btn.show()
        if not settings["permissions"]["deals_window"]["delete_discount"]:
            self.delete_discount_btn.hide()
        else:
            self.delete_discount_btn.show()
        if not settings["permissions"]["deals_window"]["delete_deal"]:
            self.delete_deal_btn.hide()
        else:
            self.delete_deal_btn.show()