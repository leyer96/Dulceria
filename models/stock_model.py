from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt, Signal
import sqlite3
from utils import Paths

class StockModel(QSqlQueryModel):
    error = Signal()
    success = Signal()
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.headers = ["Producto", "Categoría", "Cantidad en Stock"]
        self.filter = None
    
    def search(self, search_str, filter):
        self.search_str = search_str
        self.filter = filter
        query = """
            SELECT stock_test.product, product_test.category, stock_test.amount FROM stock_test
            JOIN product_test ON stock_test.product_id = product_test.id
            WHERE product_test.{} LIKE '%{}%'
            ORDER BY stock_test.amount
        """.format(filter, search_str)
        Qquery = QSqlQuery(query, db=self.db)
        print(Qquery.lastQuery())
        self.setQuery(Qquery)

    def get_all_prodcuts(self):
        query = """
            SELECT * FROM stock_test
            JOIN product_test ON stock_test.product_id = product_test.id
            ORDER BY stock_test.amount
        """
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)

    def refresh_table(self):
        if self.filter:
            query = """
                SELECT id, name, price, category, code FROM product_test
                WHERE {} LIKE '%{}%'
            """.format(self.filter, self.search_str)
            Qquery = QSqlQuery(query, db=self.db)
            self.setQuery(Qquery)

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]
