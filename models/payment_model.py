from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt
import sqlite3
from utils import Paths

class PaymentModel(QSqlQueryModel):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.headers = ["Id", "Timestamp", "Forma de pago", "Cantidad", "Nota"]
    
    def search(self, search_str, filter):
        query = """
            SELECT (id, timestamp, payment_form, amount, note) FROM payment_test
            WHERE {} LIKE '%{}%'
        """.format(filter, search_str)
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)

    def get_all_payments(self):
        query = """
            SELECT * FROM payment_test
        """
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]
