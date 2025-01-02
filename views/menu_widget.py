from PySide6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QSizePolicy
from PySide6.QtCore import Signal, Qt, QSize
from PySide6.QtGui import QIcon, QCursor
from utils import Paths

class Menu(QWidget):
    go_to_products = Signal()
    go_to_home = Signal()
    go_to_stock = Signal()
    go_to_payments = Signal()
    go_to_admin = Signal()
    go_to_deals = Signal()
    def __init__(self):
        super().__init__()
        self.go_to_products_btn = QPushButton(QIcon(Paths.icon("price-tag--arrow.png")),"Productos")
        self.go_to_home_btn = QPushButton(QIcon(Paths.icon("home--arrow.png")),"Inicio")
        self.go_to_stock_btn = QPushButton(QIcon(Paths.icon("clipboard--arrow.png")),"Stock")
        self.go_to_payments_btn = QPushButton(QIcon(Paths.icon("money--arrow.png")),"Pagos")
        self.go_to_admin_window_btn = QPushButton(QIcon(Paths.icon("computer--arrow.png")),"Admin")
        self.go_to_deals_btn = QPushButton(QIcon(Paths.icon("star.png")), "Promociones")

        self.go_to_products_btn.clicked.connect(self.go_to_products.emit)
        self.go_to_home_btn.clicked.connect(self.go_to_home.emit)
        self.go_to_stock_btn.clicked.connect(self.go_to_stock)
        self.go_to_payments_btn.clicked.connect(self.go_to_payments.emit)
        self.go_to_admin_window_btn.clicked.connect(self.go_to_admin.emit)
        self.go_to_deals_btn.clicked.connect(self.go_to_deals.emit)
        
        self.go_to_admin_window_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.go_to_products_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.go_to_home_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.go_to_stock_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.go_to_payments_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.go_to_deals_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.go_to_admin_window_btn.setCursor(QCursor(Qt.PointingHandCursor))

        layout = QVBoxLayout()
        layout.addWidget(self.go_to_home_btn)
        layout.addWidget(self.go_to_products_btn)
        layout.addWidget(self.go_to_payments_btn)
        layout.addWidget(self.go_to_stock_btn)
        layout.addWidget(self.go_to_deals_btn)
        layout.addWidget(self.go_to_admin_window_btn)

        layout.setAlignment(self.go_to_home_btn, Qt.AlignHCenter)
        layout.setAlignment(self.go_to_products_btn, Qt.AlignHCenter)
        layout.setAlignment(self.go_to_stock_btn, Qt.AlignHCenter)
        layout.setAlignment(self.go_to_payments_btn, Qt.AlignHCenter)
        layout.setAlignment(self.go_to_deals_btn, Qt.AlignHCenter)
        layout.setAlignment(self.go_to_admin_window_btn, Qt.AlignHCenter)

        layout.setSpacing(1)

        self.setLayout(layout)

        btn_size = QSize(120, 40)

        self.go_to_admin_window_btn.setFixedSize(btn_size)
        self.go_to_products_btn.setFixedSize(btn_size)
        self.go_to_home_btn.setFixedSize(btn_size)
        self.go_to_stock_btn.setFixedSize(btn_size)
        self.go_to_payments_btn.setFixedSize(btn_size)
        self.go_to_deals_btn.setFixedSize(btn_size)
        self.go_to_admin_window_btn.setFixedSize(btn_size)

        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)