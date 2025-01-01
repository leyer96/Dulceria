from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt, Signal
import sqlite3
from utils import Paths

class SearchModel(QSqlQueryModel):
    error = Signal()
    success = Signal()
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.headers = ["Id", "Producto", "Marca", "Precio", "Categoría", "Código"]
        self.filter = None
    
    def data(self, index, role):
        value = super().data(index, Qt.DisplayRole)
        if role == Qt.DisplayRole:
            if index.column() == 1 or index.column() == 2:
                capitalized_value = value.capitalize()
                return capitalized_value
            return value
    
    def search(self, search_str, filter):
        self.search_str = search_str
        self.filter = filter
        query = """
            SELECT id, name, brand, price, category, code FROM product
            WHERE {} LIKE :search_str
            LIMIT 50
        """.format(filter)
        Qquery = QSqlQuery(db=self.db)
        Qquery.prepare(query)
        Qquery.bindValue(":search_str", f"%{search_str}%")
        if not Qquery.exec():
            self.error.emit()
        else:
            self.setQuery(Qquery)
            self.success.emit()

    def get_all_prodcuts(self):
        query = """
            SELECT * FROM product
            ORDER BY NAME
            LIMIT 50
        """
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)
        self.success.emit()

    def refresh_table(self):
        if self.filter:
            self.search(self.search_str, self.filter)
        else:
            query = """
            SELECT * FROM product
            ORDER BY NAME
            LIMIT 50
            """
            Qquery = QSqlQuery(query, db=self.db)
            self.setQuery(Qquery)
            self.success.emit()

    def delete_product(self, product_id):
        con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        try:
            cur.execute("""
                DELETE FROM product WHERE id=?
            """,(product_id,))
        except sqlite3.Error as e:
            print(e)
            self.error.emit()
        else:
            con.commit()
            self.success.emit()
            self.refresh_table()

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]
