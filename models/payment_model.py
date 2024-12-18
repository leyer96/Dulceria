from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt, Signal
import sqlite3
from datetime import datetime, timedelta
from utils import Paths

class PaymentModel(QSqlQueryModel):
    error = Signal()
    success = Signal()
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.headers = ["Id", "Timestamp", "Forma de pago", "Cantidad", "Nota"]
    
    def data(self, index, role):
        value = super().data(index, Qt.DisplayRole)
        if role == Qt.DisplayRole:
            if index.column() == 1:
                dateandtime = value.split(" ")
                date = dateandtime[0]
                date_splitted = date.split("-")
                date_splitted.reverse()
                date_formatted = "-".join(date_splitted)
                time = dateandtime[1][0:5]
                formatted_dateandtime = date_formatted + " " + time
                return formatted_dateandtime
            if index.column() == 3:
                formatted_amount = "$" + str(value)
                return formatted_amount
            return value

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]
    
    def search(self, search_str, filter):
        query = """
            SELECT (id, timestamp, payment_form, amount, note) FROM payment_test
            WHERE {} LIKE :search_str
        """.format(filter)
        Qquery = QSqlQuery(db=self.db)
        Qquery.prepare(query)
        Qquery.bindValue(":search_str", f"%{search_str}%")
        if not Qquery.execute():
            self.error.emit()
        else:
            self.setQuery(Qquery)
               
    def get_todays_payment(self):
        today_date_str = datetime.today().strftime("%Y-%m-%d")
        tomorrow_date = datetime.today() + timedelta(days=1)
        tomorrow_date_str = tomorrow_date.strftime("%Y-%m-%d")
        query = """
            SELECT * FROM payment_test
            WHERE timestamp BETWEEN '{}' AND '{}'
        """.format(today_date_str, tomorrow_date_str)
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)
    
    def get_all_payments(self):
        query = """
            SELECT * FROM payment_test
        """
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)

    def search(self, date_data):
        start_date = date_data["start_date"]
        start_date_str = start_date.toString("yyyy-MM-dd")
        end_date = date_data["end_date"]
        end_date = end_date.addDays(1)
        end_date_str = end_date.toString("yyyy-MM-dd")
        query = """
            SELECT * FROM payment_test WHERE timestamp
            BETWEEN '{}' AND '{}'
        """.format(start_date_str, end_date_str)
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)
        