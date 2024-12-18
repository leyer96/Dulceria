from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt, Signal
import sqlite3
from utils import Paths, date_raw_format
from datetime import datetime, timedelta

class BatchModel(QSqlQueryModel):
    error = Signal()
    updated = Signal()
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.headers = ["Lote", "Marca", "Producto", "Categoría", "Cantidad en Lote", "Fecha de Caducidad", "Días para Caducar"]
        self.filter = None
        self.search_str = None

    def data(self, index, role):
        value = super().data(index, Qt.DisplayRole)
        if role == Qt.DisplayRole:
            if index.column() == 1 or index.column() == 2:
                return value.capitalize()
            elif index.column() == 5:
                date_info = value.split("-")
                date_info.reverse()
                return "-".join(date_info)
            elif index.column() == 6:
                expiration_date_str = super().data(super().index(index.row(),5), Qt.DisplayRole)
                expiration_date_obj = datetime.strptime(expiration_date_str, date_raw_format)
                delta = expiration_date_obj - datetime.today()
                delta_days = delta.days
                if delta_days < 0:
                    return "CADUCADO"
                return delta_days
            return value
            
    def columnCount(self, index):
        return len(self.headers)
    
    def search(self, search_str, filter):
        self.search_str = search_str
        self.filter = filter
        query = """
            SELECT batch_test.id, product_test.brand, product_test.name, product_test.category, batch_test.amount, batch_test.expiration_date 
            FROM batch_test
            JOIN product_test ON batch_test.product_id = product_test.id
            WHERE product_test.{} LIKE :search_term AND batch_test.show = 1
            ORDER BY batch_test.expiration_date
        """.format(filter)
        Qquery = QSqlQuery(db=self.db)
        Qquery.prepare(query)
        Qquery.bindValue(":search_term", f'%{search_str}%')
        if not Qquery.exec():
            self.error.emit()
        else:
            self.setQuery(Qquery)

    def get_all_batchs(self):
        query = """
            SELECT batch_test.id, product_test.brand, product_test.name, product_test.category, batch_test.amount, batch_test.expiration_date 
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
            SELECT batch_test.id, product_test.brand, product_test.name, product_test.category, batch_test.amount, batch_test.expiration_date 
            FROM batch_test
            JOIN product_test ON stock_test.product_id = product_test.id
            WHERE product_test.{} like :search_term
            ORDER BY batch_test.expiration_date
        """.format(self.filter)
            Qquery = QSqlQuery(db=self.db)
            Qquery.prepare(query)
            Qquery.bindValue(":search_term", f"%{self.search_str}")
            self.setQuery(Qquery)
        else:
            self.get_all_batchs()

    def update_batch_show_status(self, batch_id):
        con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        try:
            cur.execute("UPDATE batch_test SET show = ? WHERE id = ?", (0, batch_id))
        except sqlite3.Error as e:
            print(e)
            self.error.emit()
        else:
            con.commit()
            self.updated.emit()
            self.refresh_table()

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]
 