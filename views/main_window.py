from PySide6.QtWidgets import QMainWindow, QStackedLayout, QWidget
from views.home.home_window import HomeWindow


class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()

        self.resize(700, 500)

        home_widget = HomeWindow(db)
        container = QWidget()
        container_layout = QStackedLayout()
        container_layout.addWidget(home_widget)
        container.setLayout(container_layout)
        
        self.setCentralWidget(container)
        self.show()