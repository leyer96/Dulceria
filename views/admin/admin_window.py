from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QPushButton,
    QComboBox,
    QLabel,
    QSpinBox,
    QWidget,
    QGridLayout,
    QSizePolicy,
    QMessageBox,
    QFormLayout,
    QLineEdit
)
from PySide6.QtCore import Qt, Signal
from utils import Paths, load_settings, save_settings
import json

class AdminWindow(QWidget):
    new_settings = Signal()
    def __init__(self, db, menu):
        super().__init__()
        self.menu = menu
        self.db = db

        # PERMISSIONS

        title_label = QLabel("Admin")
        title_label.setStyleSheet("font-size: 30px; font-weight: bold")

        permissions_title = QLabel("Permisos")   
        permissions_title.setStyleSheet("font-size: 20px; font-weight: bold")

        col1_title = QLabel("Productos")
        self.product_add_option = QCheckBox("Añadir")
        self.product_edit_option = QCheckBox("Editar")
        self.product_delete_option = QCheckBox("Eliminar")

        col2_title = QLabel("Stock")
        self.stock_edit_option = QCheckBox("Modificar stock")
        self.stock_add_option = QCheckBox("Añadir lote")
        self.stock_resolve_option = QCheckBox("Resolver")

        col3_title = QLabel("Pagos")
        self.payment_view_option = QCheckBox("Ver pagos")

        col1_layout = QVBoxLayout()
        col1_layout.addWidget(col1_title)
        col1_layout.addWidget(self.product_add_option)
        col1_layout.addWidget(self.product_edit_option)
        col1_layout.addWidget(self.product_delete_option)

        col2_layout = QVBoxLayout()
        col2_layout.addWidget(col2_title)
        col2_layout.addWidget(self.stock_edit_option)
        col2_layout.addWidget(self.stock_add_option)
        col2_layout.addWidget(self.stock_resolve_option)

        col3_layout = QVBoxLayout()
        col3_layout.addWidget(col3_title)
        col3_layout.addWidget(self.payment_view_option)

        save_permissions_btn = QPushButton("Guardar permisos")
        save_permissions_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        options_layout = QHBoxLayout()
        options_layout.addLayout(col1_layout)
        options_layout.addLayout(col2_layout)
        options_layout.addLayout(col3_layout)

        options_layout.setAlignment(col1_layout, Qt.AlignTop)
        options_layout.setAlignment(col2_layout, Qt.AlignTop)
        options_layout.setAlignment(col3_layout, Qt.AlignTop)

        # CATEGORIES

        categories_title = QLabel("Categorías de productos")
        categories_title.setStyleSheet("font-size: 20px; font-weight: bold")

        self.new_category_input = QLineEdit()
        add_category_btn = QPushButton("Agregar")
        add_category_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        add_category_layout = QHBoxLayout()
        add_category_layout.addWidget(QLabel("Añadir Categoría:"))
        add_category_layout.addWidget(self.new_category_input)
        add_category_layout.addWidget(add_category_btn)
        
        self.select_category_input = QComboBox()
        delete_category_btn = QPushButton("Borrar")
        delete_category_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        delete_category_layout = QHBoxLayout()
        delete_category_layout.addWidget(QLabel("Eliminar Categoría:"))
        delete_category_layout.addWidget(self.select_category_input)
        delete_category_layout.addWidget(delete_category_btn)

        hidden_layout = QVBoxLayout()
        hidden_layout.addWidget(permissions_title)
        hidden_layout.addLayout(options_layout)
        hidden_layout.addWidget(save_permissions_btn)
        hidden_layout.addWidget(categories_title)
        hidden_layout.addLayout(add_category_layout)
        hidden_layout.addWidget(add_category_btn)
        hidden_layout.addLayout(delete_category_layout)
        hidden_layout.addWidget(delete_category_btn)

        hidden_layout.setAlignment(save_permissions_btn, Qt.AlignHCenter)
        hidden_layout.setAlignment(add_category_btn, Qt.AlignHCenter)
        hidden_layout.setAlignment(delete_category_btn, Qt.AlignHCenter)

        self.hidden_widget = QWidget()
        self.hidden_widget.setLayout(hidden_layout)
        self.hidden_widget.hide()

        # SIGNALS
        save_permissions_btn.clicked.connect(self.save_permissions)
        add_category_btn.clicked.connect(self.add_category)
        delete_category_btn.clicked.connect(self.delete_category)

        # LOGIN
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        form = QFormLayout()
        form.addRow("Contraseña:", self.password_input)
        login_btn = QPushButton("Ingresar")

        login_layout = QVBoxLayout()
        login_layout.addLayout(form)
        login_layout.addWidget(login_btn)

        self.login_widget = QWidget()
        self.login_widget.setLayout(login_layout)

        login_btn.clicked.connect(self.authenticate)
    
        # GRID
        grid = QGridLayout()
        grid.addWidget(title_label, 0, 0, 1, 9)
        grid.addWidget(self.hidden_widget, 1, 0, 4, 9)
        grid.addWidget(self.login_widget, 1, 0, 2, 9)
        grid.addWidget(self.menu, 2, 9, 5, 3)
        self.setLayout(grid)

        # CONFIG
        self.menu.go_to_admin_window_btn.setEnabled(False)
        self.load_settings()

    def authenticate(self):
        password = self.password_input.text()
        if password == "123":
            self.hidden_widget.show()
            self.login_widget.hide()

    def hide_content(self):
        self.hidden_widget.hide()
        self.login_widget.show()
        self.password_input.clear()
    
    def load_settings(self):
        settings = load_settings()
        self.settings = settings
        if settings["permissions"]["products_window"]["add"]:
            self.product_add_option.setChecked(True)
        if settings["permissions"]["products_window"]["edit"]:
            self.product_edit_option.setChecked(True)
        if settings["permissions"]["products_window"]["delete"]:
            self.product_delete_option.setChecked(True)
        if settings["permissions"]["stock_window"]["edit"]:
            self.stock_edit_option.setChecked(True)
        if settings["permissions"]["stock_window"]["add"]:
            self.stock_add_option.setChecked(True)
        if settings["permissions"]["stock_window"]["resolve"]:
            self.stock_resolve_option.setChecked(True)
        if settings["permissions"]["payments_window"]["view"]:
            self.payment_view_option.setChecked(True)
        self.select_category_input.addItems(settings["gui"]["product_categories"])
    
    def save_permissions(self):
        self.settings["permissions"]["products_window"]["add"] = self.product_add_option.isChecked()
        self.settings["permissions"]["products_window"]["edit"] = self.product_edit_option.isChecked()
        self.settings["permissions"]["products_window"]["delete"] = self.product_delete_option.isChecked()
        self.settings["permissions"]["stock_window"]["edit"] = self.stock_edit_option.isChecked()
        self.settings["permissions"]["stock_window"]["add"] = self.stock_add_option.isChecked()
        self.settings["permissions"]["stock_window"]["resolve"] = self.stock_resolve_option.isChecked()
        self.settings["permissions"]["payments_window"]["view"] = self.payment_view_option.isChecked()
        saved = save_settings(self.settings)
        if saved:
            QMessageBox.information(self, "Permisos Guardados", "Los permisos han sido guardados con éxito")
            self.new_settings.emit()
        else:
            QMessageBox.information(self, "Error", "Ha ocurrido un error. Contacte al administrador")

    def add_category(self):
        new_category = self.new_category_input.text()
        if new_category:
            if new_category not in self.settings["gui"]["product_categories"]:
                self.settings["gui"]["product_categories"].append(new_category)
                saved = save_settings(self.settings)
                if saved:
                    QMessageBox.information(self, "Categoría Guardadada", "Categoría agregada")
                    self.select_category_input.addItem(new_category)
                    self.new_category_input.clear()
                    self.new_settings.emit()
                else:
                    QMessageBox.information(self, "Error", "Ha ocurrido un error. Contacte al administrador")

    def delete_category(self):
        if len(self.settings["gui"]["product_categories"]) > 2:
            index = self.select_category_input.currentIndex()
            if index != 0:
                del(self.settings["gui"]["product_categories"][index])
                saved = save_settings(self.settings)
                if saved:
                    QMessageBox.information(self, "Categoría Eliminada", "Categoría eliminada.")
                    self.select_category_input.removeItem(index)
                    self.select_category_input.setCurrentIndex(0)
                    self.new_settings.emit()
                else:
                    QMessageBox.information(self, "Error", "Ha ocurrido un error. Contacte al administrador")
        else:
            QMessageBox.warning(self, "Error", "Debe haber por lo menos una categoría guardada. ")
        
        