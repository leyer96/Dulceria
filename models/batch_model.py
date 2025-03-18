from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt, Signal
import sqlite3
from utils import Paths, get_days_till_expiration, no_exipration_date_date

class BatchModel(QSqlQueryModel):
    error = Signal()
    updated = Signal()
    success = Signal()
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.headers = ["Lote", "Marca", "Producto", "Categoría", "Cantidad en Lote", "Fecha de Caducidad", "Días para Caducar"]
        self.filter = None
        self.search_str = ""

    def data(self, index, role):
        value = super().data(index, Qt.DisplayRole)
        if role == Qt.DisplayRole:
            if index.column() == 1 or index.column() == 2:
                return value.capitalize()
            elif index.column() == 5:
                if value == no_exipration_date_date:
                    return ""
                date_info = value.split("-")
                date_info.reverse()
                return "-".join(date_info)
            elif index.column() == 6:
                expiration_date_str = super().data(super().index(index.row(),5), Qt.DisplayRole)
                return get_days_till_expiration(expiration_date_str)
            return value
            
    def columnCount(self, index):
        return len(self.headers)
    
    def search(self, search_str, filter):
        self.search_str = search_str
        self.filter = filter
        query = """
            SELECT batch.id, product.name, product.brand, product.category, batch.amount, batch.expiration_date 
            FROM batch
            JOIN product ON batch.product_id = product.id
            WHERE product.{} LIKE :search_term AND batch.show = 1
            ORDER BY batch.expiration_date
            LIMIT 50
        """.format(filter)
        Qquery = QSqlQuery(db=self.db)
        Qquery.prepare(query)
        Qquery.bindValue(":search_term", f'%{search_str}%')
        if not Qquery.exec():
            self.error.emit()
        else:
            if Qquery.first():
                self.setQuery(Qquery)
            self.success.emit()

    def get_all_batchs(self):
        query = """
            SELECT batch.id, product.name, product.brand, product.category, batch.amount, batch.expiration_date 
            FROM batch
            JOIN product ON batch.product_id = product.id
            WHERE batch.show = 1
            ORDER BY batch.expiration_date
            LIMIT 50
        """
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)
        self.success.emit()

    def refresh_table(self):
        if self.filter:
            self.search(self.search_str, self.filter)
        else:
            self.get_all_batchs()

    def update_batch_show_status(self, batch_id):
        con = sqlite3.connect(Paths.test("db.db"))
        # con = sqlite3.connect(Paths.db())
        cur = con.cursor()
        try:
            cur.execute("UPDATE batch SET show = ? WHERE id = ?", (0, batch_id))
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
 