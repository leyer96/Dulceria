from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt
import sqlite3
from utils import Paths

class SearchModel(QSqlQueryModel):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.headers = ["Id", "Producto", "Precio", "Código", "Categoría"]
        self.create_test_table()

    def create_test_table(self):
        print(Paths.db())
        con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS product_test (
                id INTEGER PRIMARY KEY AUTOINCREMENT,  
                name TEXT NOT NULL, 
                price FLOAT NOT NULL,  
                category TEXT NOT NULL,
                code TEXT
            );
            """)
    
    def search(self, search_str, filter):
        query = """
            SELECT id, name, price, category FROM product_test
            WHERE {} LIKE '%{}%'
        """.format(filter, search_str)
        print(query)
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]
