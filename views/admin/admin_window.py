from PySide6.QtWidgets import (
    QVBoxLayout,
    QHBoxLayout,
    QCheckBox,
    QFileDialog,
    QPushButton,
    QComboBox,
    QLabel,
    QWidget,
    QSizePolicy,
    QMessageBox,
    QLineEdit,
    QFormLayout
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap
from views.dialogs.authorize import AuthorizeDialog
from utils import load_settings, save_settings, Paths
import os
import shutil

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
        self.stock_add_deal_option = QCheckBox("Añadir promocióm")
        self.stock_add_discount_option = QCheckBox("Añadir descuento")

        col3_title = QLabel("Pagos")
        self.payment_view_option = QCheckBox("Ver pagos")

        col4_title = QLabel("Promociones")
        self.deal_delete_discount_option = QCheckBox("Eliminar descuento")
        self.deal_delete_deal_option = QCheckBox("Eliminar promoción")

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
        col2_layout.addWidget(self.stock_add_discount_option)
        col2_layout.addWidget(self.stock_add_deal_option)

        col3_layout = QVBoxLayout()
        col3_layout.addWidget(col3_title)
        col3_layout.addWidget(self.payment_view_option)

        col4_layout = QVBoxLayout()
        col4_layout.addWidget(col4_title)
        col4_layout.addWidget(self.deal_delete_discount_option)
        col4_layout.addWidget(self.deal_delete_deal_option)

        save_permissions_btn = QPushButton("Guardar permisos")
        save_permissions_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        options_layout = QHBoxLayout()
        options_layout.addLayout(col1_layout)
        options_layout.addLayout(col2_layout)
        options_layout.addLayout(col3_layout)
        options_layout.addLayout(col4_layout)

        options_layout.setAlignment(col1_layout, Qt.AlignTop)
        options_layout.setAlignment(col2_layout, Qt.AlignTop)
        options_layout.setAlignment(col3_layout, Qt.AlignTop)
        options_layout.setAlignment(col4_layout, Qt.AlignTop)

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

        # EXPORT DB
        export_db_title = QLabel("Datos")
        export_db_title.setStyleSheet("font-size: 20px; font-weight: bold")
        export_db_btn = QPushButton("Exportar Datos")
        
        # CHANGE PASSWORD

        password_title = QLabel("Contraseña")
        password_title.setStyleSheet("font-size: 20px; font-weight: bold")

        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.Password)
        self.new_password_input_repeat = QLineEdit()
        self.new_password_input_repeat.setEchoMode(QLineEdit.Password)

        reset_password_form = QFormLayout()
        reset_password_form.addRow("Contraseña nueva:", self.new_password_input)
        reset_password_form.addRow("Repetir contraseña:", self.new_password_input_repeat)

        reset_password_btn = QPushButton("Cambiar Contraseña")
        reset_password_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        
        # HIDDEN CONTENT WIDGET
        hidden_layout = QVBoxLayout()
        hidden_layout.addWidget(permissions_title)
        hidden_layout.addLayout(options_layout)
        hidden_layout.addWidget(save_permissions_btn)
        hidden_layout.addWidget(categories_title)
        hidden_layout.addLayout(add_category_layout)
        hidden_layout.addWidget(add_category_btn)
        hidden_layout.addLayout(delete_category_layout)
        hidden_layout.addWidget(delete_category_btn)
        hidden_layout.addWidget(export_db_title)
        hidden_layout.addWidget(export_db_btn)
        hidden_layout.addWidget(password_title)
        hidden_layout.addLayout(reset_password_form)
        hidden_layout.addWidget(reset_password_btn)

        hidden_layout.setAlignment(save_permissions_btn, Qt.AlignHCenter)
        hidden_layout.setAlignment(add_category_btn, Qt.AlignHCenter)
        hidden_layout.setAlignment(delete_category_btn, Qt.AlignHCenter)
        hidden_layout.setAlignment(reset_password_btn, Qt.AlignHCenter)

        self.hidden_widget = QWidget()
        self.hidden_widget.setLayout(hidden_layout)
        self.hidden_widget.hide()

        # SIGNALS
        save_permissions_btn.clicked.connect(self.save_permissions)
        add_category_btn.clicked.connect(self.add_category)
        delete_category_btn.clicked.connect(self.delete_category)
        reset_password_btn.clicked.connect(self.validate_passwords)
        export_db_btn.clicked.connect(self.authorize_export)

        # LOGIN
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        login_btn = QPushButton("Ingresar")
        login_btn.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)

        login_layout = QHBoxLayout()
        login_layout.addWidget(QLabel("Contraseña: "))
        login_layout.addWidget(self.password_input)
        login_layout.addWidget(login_btn)

        login_layout.setAlignment(login_btn, Qt.AlignHCenter)

        self.login_widget = QWidget()
        self.login_widget.setLayout(login_layout)

        login_btn.clicked.connect(self.authenticate)
    
        # LOGO
        logo_label = QLabel()
        logo_pixmap = QPixmap(Paths.image("dulceria_logo.png")).scaledToWidth(100)
        logo_label.setPixmap(logo_pixmap)
        
        # LAYOUT
        layout = QHBoxLayout()
        left_layout = QVBoxLayout()
        left_layout.addWidget(title_label)
        left_layout.addWidget(self.hidden_widget)
        left_layout.addWidget(self.login_widget)

        right_layout = QVBoxLayout()
        right_layout.addWidget(logo_label)
        right_layout.addWidget(self.menu)
        right_layout.insertSpacing(0, 30)
        right_layout.addStretch()
        right_layout.setAlignment(self.menu, Qt.AlignTop)
        right_layout.setAlignment(logo_label,Qt.AlignHCenter)
        
        layout.addLayout(left_layout)
        layout.addLayout(right_layout)

        layout.setAlignment(left_layout, Qt.AlignTop)
        layout.setStretch(0, 4)
        layout.setStretch(1, 1)

        self.setLayout(layout)

        # CONFIG
        self.menu.go_to_admin_window_btn.setEnabled(False)
        self.load_settings()

    def authenticate(self):
        password = self.password_input.text()
        if password == self.settings["admin"]["password"] or password == self.settings["developer"]["password"]:
            self.hidden_widget.show()
            self.login_widget.hide()

    def hide_content(self):
        self.hidden_widget.hide()
        self.login_widget.show()
        self.password_input.clear()

    def validate_passwords(self):
        password1 = self.new_password_input.text()
        password2 = self.new_password_input_repeat.text()
        if password1 == password2:
            dlg = AuthorizeDialog()
            dlg.authorized.connect(lambda: self.reset_password(password1))
            dlg.exec()
        else:
            QMessageBox.information(self, "Contraseñas inválidas", "Las contraseñas no son iguales.")

    def reset_password(self, password):
        self.settings["admin"]["password"] = password
        saved = save_settings(self.settings)
        if saved:
            QMessageBox.information(self, "Contraseña Guardada", "La contraseña se actualizó con éxito")
            self.new_password_input.clear()
            self.new_password_input_repeat.clear()
        else:
            QMessageBox.information(self, "Error", "Ha ocurrido un error. Contacte al administrador")
    
    def load_settings(self):
        settings = load_settings()
        self.settings = settings
        if not settings["permissions"]["payments_window"]["view"]:
            self.menu.go_to_payments_btn.hide()
        else:
            self.menu.go_to_payments_btn.show()
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
        if settings["permissions"]["stock_window"]["add_discount"]:
            self.stock_add_discount_option.setChecked(True)
        if settings["permissions"]["stock_window"]["add_deal"]:
            self.stock_add_deal_option.setChecked(True)
        if settings["permissions"]["payments_window"]["view"]:
            self.payment_view_option.setChecked(True)
        if settings["permissions"]["deals_window"]["delete_deal"]:
            self.deal_delete_deal_option.setChecked(True)
        if settings["permissions"]["deals_window"]["delete_discount"]:
            self.deal_delete_discount_option.setChecked(True)
        self.select_category_input.addItems(settings["gui"]["product_categories"])
    
    def save_permissions(self):
        self.settings["permissions"]["products_window"]["add"] = self.product_add_option.isChecked()
        self.settings["permissions"]["products_window"]["edit"] = self.product_edit_option.isChecked()
        self.settings["permissions"]["products_window"]["delete"] = self.product_delete_option.isChecked()
        self.settings["permissions"]["stock_window"]["edit"] = self.stock_edit_option.isChecked()
        self.settings["permissions"]["stock_window"]["add"] = self.stock_add_option.isChecked()
        self.settings["permissions"]["stock_window"]["resolve"] = self.stock_resolve_option.isChecked()
        self.settings["permissions"]["stock_window"]["add_discount"] = self.stock_add_discount_option.isChecked()
        self.settings["permissions"]["stock_window"]["add_deal"] = self.stock_add_deal_option.isChecked()
        self.settings["permissions"]["payments_window"]["view"] = self.payment_view_option.isChecked()
        self.settings["permissions"]["deals_window"]["delete_deal"] = self.deal_delete_deal_option.isChecked()
        self.settings["permissions"]["deals_window"]["delete_discount"] = self.deal_delete_discount_option.isChecked()
        saved = save_settings(self.settings)
        if saved:
            QMessageBox.information(self, "Permisos Guardados", "Los permisos han sido guardados con éxito")
            self.new_settings.emit()
            if self.settings["permissions"]["payments_window"]["view"]:
                self.menu.go_to_payments_btn.show()
            else:
                self.menu.go_to_payments_btn.hide()
        else:
            QMessageBox.information(self, "Error", "Ha ocurrido un error. Contacte al administrador")

    def add_category(self):
        new_category = self.new_category_input.text().strip()
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
            else:
                QMessageBox.information(self, "Categoría Duplicada", "Esta categoría ya existe.")
    
    def delete_category(self):
        if len(self.settings["gui"]["product_categories"]) > 2:
            text = self.select_category_input.currentText()
            if text == "Granel" or text == "Otro":
                QMessageBox.information(self, "Categoría Esencial", "Esta categoría no puede ser eliminada")
                return
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
    
    def authorize_export(self):
        dlg = AuthorizeDialog()
        dlg.authorized.connect(self.export_app_data)
        dlg.exec()
    
    def export_app_data(self):
        dirname = QFileDialog.getExistingDirectory(self, "Seleccionar Folder")
        if dirname:
            try:
                db_datafile = Paths.test("db.db")
                settings_datafile = Paths.setting("settings.json")

                os.makedirs(dirname, exist_ok=True)

                db_destination_file = os.path.join(dirname, "db.db")
                settings_destination_file = os.path.join(dirname, "settings.json")

                shutil.copy(db_datafile, db_destination_file)
                shutil.copy(settings_datafile, settings_destination_file)
            except Exception as e:
                print(e)