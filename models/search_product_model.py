from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt, Signal
import sqlite3
from utils import Paths

class SearchModel(QSqlQueryModel):
    error = Signal()
    success = Signal()
    product_deleted = Signal()
    no_record = Signal()
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.headers = ["Id", "Producto", "Marca", "Precio", "Categoría", "Código"]
        self.filter = None
    
    def data(self, index, role):
        value = super().data(index, Qt.DisplayRole)
        if role == Qt.DisplayRole:
            col = index.column()
            if col == 1 or col == 2:
                capitalized_value = value.capitalize()
                return capitalized_value
            elif col == 3:
                value = str(value) + " $"
                product_type = super().data(self.index(index.row(), 4), Qt.DisplayRole)
                if product_type == "Granel":
                    value += " x gr."
            return value
    
    def search(self, search_str, filter, show_msg=True):
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
            if not Qquery.first():
                if show_msg:
                    self.no_record.emit()
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
            self.search(self.search_str, self.filter, show_msg=False)
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
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
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
            self.product_deleted.emit()
            self.refresh_table()

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]
