from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt, Signal
import sqlite3
from utils import Paths

class BatchModel(QSqlQueryModel):
    error = Signal()
    updated = Signal()
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.headers = ["ID", "Producto", "Categoría", "Cantidad en Lote", "Fecha de Caducidad"]
        self.filter = None

    def data(self, index, role):
        value = super().data(index, Qt.DisplayRole)
        if role == Qt.DisplayRole:
            if index.column() == 4:
                date_info = value.split("-")
                date_info.reverse()
                return "-".join(date_info)
            else:
                return value
    
    def search(self, search_str, filter):
        self.search_str = search_str
        self.filter = filter
        query = """
            SELECT batch_test.id, batch_test.product, product_test.category, batch_test.amount, batch_test.expiration_date 
            FROM batch_test
            JOIN product_test ON batch_test.product_id = product_test.id
            WHERE product_test.{} LIKE '%{}%' AND batch_test.show = 1
            ORDER BY batch_test.expiration_date
        """.format(filter, search_str)
        Qquery = QSqlQuery(query, db=self.db)
        print(Qquery.lastQuery())
        self.setQuery(Qquery)

    def get_all_batchs(self):
        query = """
            SELECT batch_test.id, batch_test.product, product_test.category, batch_test.amount, batch_test.expiration_date 
            FROM batch_test
            JOIN product_test ON batch_test.product_id = product_test.id
            ORDER BY batch_test.expiration_date
            LIMIT 20
        """
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)

    def refresh_table(self):
        if self.filter:
            query = """
            SELECT batch_test.id, batch_test.product, product_test.category, batch_test.amount, batch_test.expiration_date 
            FROM batch_test
            JOIN product_test ON stock_test.product_id = product_test.id
            WHERE product_test.{} like '%{}%'
            ORDER BY batch_test.expiration_date
        """.format(self.filter, self.search_str)
            Qquery = QSqlQuery(query, db=self.db)
            self.setQuery(Qquery)
        else:
            self.get_all_batchs()

    def update_batch_show_status(self, batch_id):
        con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        try:
            cur.execute("UPDATE batch_test SET show = ? WHERE id = ?", (0, batch_id))
            con.commit()
            self.updated.emit()
        except:
            self.error.emit()

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]
 