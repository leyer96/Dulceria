from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt, Signal
import sqlite3
from utils import Paths

class BatchModel(QSqlQueryModel):
    error = Signal()
    success = Signal()
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.headers = ["ID", "Producto", "Categoría", "Cantidad en Lote", "Fecha de Caducidad"]
        self.filter = None
    
    def search(self, search_str, filter):
        self.search_str = search_str
        self.filter = filter
        query = """
            SELECT batch_test.id, batch_test.product, product_test.category, batch_test.amount, batch_test.expiration_date FROM batch_test
            JOIN product_test ON batch_test.product_id = product_test.id
            WHERE product_test.{} LIKE '%{}%' AND batch_test.show = 1
            ORDER BY batch_test.expiration_date
        """.format(filter, search_str)
        Qquery = QSqlQuery(query, db=self.db)
        print(Qquery.lastQuery())
        self.setQuery(Qquery)

    def get_all_batchs(self):
        query = """
            SELECT * FROM batch_test
            JOIN product_test ON batch_test.product_id = product_test.id
            WHERE batch_test.id = 1
            ORDER BY DESC batch_test.expiration_date
        """
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)

    def update_batch_show_status(self, batch_id):
        con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        cur.execute("UPDATE batch_test SET show = ? WHERE id = ?", (0, batch_id))
        con.commit()


    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]
 