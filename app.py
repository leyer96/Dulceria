from PySide6.QtWidgets import (
    QApplication
)
from views.main_window import MainWindow
from PySide6.QtSql import QSqlDatabase
from utils import Paths

app = QApplication([])

# ----- USAR SQLITE ??? -----
db = QSqlDatabase("QSQLITE") 
db.setDatabaseName(Paths.db()) 
db.open()
# ---------------------------

w = MainWindow(db)

app.exec()