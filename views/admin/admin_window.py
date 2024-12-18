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
from utils import Paths, load_settings
import json

class AdminWindow(QWidget):
    new_settings = Signal()
    def __init__(self, db, menu):
        super().__init__()
        self.menu = menu
        self.db = db

        title_label = QLabel("Admin")
        title_label.setStyleSheet("font-size: 30px; font-weight: bold")   

        col1_title = QLabel("Productos")
        self.product_add_option = QCheckBox("Añadir")
        self.product_edit_option = QCheckBox("Editar")
        self.product_delete_option = QCheckBox("Eliminar")

        col2_title = QLabel("Stock")
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

        options_v_layout = QVBoxLayout()
        options_v_layout.addLayout(options_layout)
        options_v_layout.addWidget(save_permissions_btn)

        options_v_layout.setAlignment(save_permissions_btn, Qt.AlignHCenter)

        self.hidden_widget = QWidget()
        self.hidden_widget.setLayout(options_v_layout)
        self.hidden_widget.hide()

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
    
        filler = QWidget()

        grid = QGridLayout()
        grid.addWidget(title_label, 0, 0, 1, 9)
        grid.addWidget(self.hidden_widget, 1, 0, 2, 9)
        grid.addWidget(self.login_widget, 1, 0, 2, 9)
        grid.addWidget(self.menu, 2, 9, 5, 3)
        grid.addWidget(filler, 6, 0, 6, 12)
        self.setLayout(grid)

        self.menu.go_to_admin_window_btn.setEnabled(False)
        save_permissions_btn.clicked.connect(self.save_permissions)
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
        if settings["permissions"]["products_window"]["add"]:
            self.product_add_option.setChecked(True)
        if settings["permissions"]["products_window"]["edit"]:
            self.product_edit_option.setChecked(True)
        if settings["permissions"]["products_window"]["delete"]:
            self.product_delete_option.setChecked(True)
        if settings["permissions"]["stock_window"]["add"]:
            self.stock_add_option.setChecked(True)
        if settings["permissions"]["stock_window"]["resolve"]:
            self.stock_resolve_option.setChecked(True)
        if settings["permissions"]["payments_window"]["view"]:
            self.payment_view_option.setChecked(True)
    
    def save_permissions(self):
        settings = load_settings()
        settings["permissions"]["products_window"]["add"] = self.product_add_option.isChecked()
        settings["permissions"]["products_window"]["edit"] = self.product_edit_option.isChecked()
        settings["permissions"]["products_window"]["delete"] = self.product_delete_option.isChecked()
        settings["permissions"]["stock_window"]["add"] = self.stock_add_option.isChecked()
        settings["permissions"]["stock_window"]["resolve"] = self.stock_resolve_option.isChecked()
        settings["permissions"]["payments_window"]["view"] = self.payment_view_option.isChecked()
        with open(Paths.setting("settings.json"), "w") as f:
            dump = json.dumps(settings)
            try:
                f.write(dump)
            except Exception as e:
                print(e)
                QMessageBox.information(self, "Error", "Ha ocurrido un error. Contacte al administrador")
            else:
                f.close()
                QMessageBox.information(self, "Permisos Guardados", "Los permisos han sido guardados con éxito")
                self.new_settings.emit()
        