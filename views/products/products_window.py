from PySide6.QtWidgets import (
    QTableView,
    QVBoxLayout,
    QAbstractItemView,
    QHeaderView,
    QPushButton,
    QWidget,
    QHBoxLayout,
    QMessageBox,
    QLabel
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon, QPixmap
from views.home.search_widget import SearchWidget
from models.search_product_model import SearchModel
from views.dialogs.add_product import AddItemDialog
from views.dialogs.edit_product import EditItemDialog
from views.dialogs.question import QuestionDialog
from utils import Paths, load_settings

class ProductsWindow(QWidget):
    product_created = Signal()
    product_edited = Signal()
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
        title = QLabel("Productos")
        
        # CONFIG
        self.table.setModel(self.model)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.model.get_all_prodcuts()
        self.edit_product_btn.setEnabled(False)
        self.delete_product_btn.setEnabled(False)
        self.menu.go_to_products_btn.setEnabled(False)
        title.setStyleSheet("font-size: 30px; font-weight: bold")
        self.selected_row = -1

         # SIGNALS
        self.search_widget.search_btn.clicked.connect(self.handle_search)
        self.search_widget.search_input.returnPressed.connect(self.handle_search)
        self.table.clicked.connect(self.on_clicked_row)
        self.add_product_btn.clicked.connect(self.open_add_dialog)
        self.edit_product_btn.clicked.connect(lambda: self.open_edit_dialog(self.selected_row))
        self.delete_product_btn.clicked.connect(lambda: self.delete_product(self.selected_row))
        self.model.success.connect(lambda: self.edit_product_btn.setEnabled(False))
        self.model.success.connect(lambda: self.delete_product_btn.setEnabled(False))
        self.model.no_record.connect(lambda: QMessageBox.information(self, "Sin Emparejamiento", "No se encontró producto con la información proporcionada."))
        
        # LOGO
        logo_label = QLabel()
        logo_pixmap = QPixmap(Paths.image("dulceria_logo.png")).scaledToWidth(100)
        logo_label.setPixmap(logo_pixmap)
        
        # LAYOUT
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.add_product_btn)
        buttons_layout.addWidget(self.edit_product_btn)
        buttons_layout.addWidget(self.delete_product_btn)

        layout = QHBoxLayout()

        left_layout = QVBoxLayout()
        left_layout.addWidget(title)
        left_layout.addWidget(self.search_widget)
        left_layout.addWidget(self.table)
        left_layout.addLayout(buttons_layout)

        right_layout = QVBoxLayout()
        right_layout.addWidget(logo_label)
        right_layout.addWidget(self.menu)
        right_layout.insertSpacing(0, 30)
        right_layout.addStretch()
        right_layout.setAlignment(self.menu, Qt.AlignTop)
        right_layout.setAlignment(logo_label,Qt.AlignHCenter)

        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        layout.setStretch(0, 4)
        layout.setStretch(1, 1)

        self.setLayout(layout)

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
        self.model.search(str, filter)
        if self.search_widget.filter_by_code.isChecked():
            self.search_widget.search_input.setText("")

    def on_clicked_row(self, index):
        self.selected_row = index.row()
        if self.selected_row > -1:
            if not self.edit_product_btn.isEnabled():
                self.edit_product_btn.setEnabled(True)
                self.delete_product_btn.setEnabled(True)
    
    def open_add_dialog(self):
        dlg = AddItemDialog(self.db, self.categories)
        dlg.saved.connect(self.model.refresh_table)
        dlg.saved.connect(self.product_created.emit)
        dlg.exec()
    
    def open_edit_dialog(self, row):
        if row != None:
            product_id = self.model.data(self.model.index(row, 0), Qt.DisplayRole)
            dlg = AddItemDialog(self.db, self.categories, product_id=product_id)
            dlg.saved.connect(self.model.refresh_table)
            dlg.saved.connect(self.product_edited.emit)
            dlg.exec()
        
    def delete_product(self, row):
        if row != None:
            question_dlg = QuestionDialog(f"¿Estás seguro que quieres eliminar: {self.model.data(self.model.index(row, 1), Qt.DisplayRole)}?")
            product_id = int(self.model.data(self.model.index(row, 0), Qt.DisplayRole))
            question_dlg.accepted.connect(lambda: self.model.delete_product(product_id))
            question_dlg.accepted.connect(self.model.refresh_table)
            question_dlg.exec()

    def load_settings(self):
        settings = load_settings()
        if not settings["permissions"]["payments_window"]["view"]:
            self.menu.go_to_payments_btn.hide()
        else:
            self.menu.go_to_payments_btn.show()
        if not settings["permissions"]["products_window"]["add"]:
            self.add_product_btn.hide()
        else:
            self.add_product_btn.show()
        if not settings["permissions"]["products_window"]["edit"]:
            self.edit_product_btn.hide()
        else:
            self.edit_product_btn.show()
        if not settings["permissions"]["products_window"]["delete"]:
            self.delete_product_btn.hide()
        else:
            self.delete_product_btn.show()
        self.categories = settings["gui"]["product_categories"]
