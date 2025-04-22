from PySide6.QtWidgets import (
    QApplication
)
from views.main_window import MainWindow
from PySide6.QtSql import QSqlDatabase
from utils import Paths

app = QApplication([])

db = QSqlDatabase("QSQLITE") 
db.setDatabaseName(Paths.test("db.db")) 
# db.setDatabaseName(Paths.db()) 
db.open()

try: 
    from ctypes import windll # Only exists on Windows.
    myappid = "aigenappz.dulceria.gui.v1"
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

w = MainWindow(db)

app.exec()