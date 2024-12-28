from PySide6.QtSql import (
    QSqlQueryModel,
    QSqlQuery
)
from PySide6.QtCore import Signal, Qt
from utils import get_datetime_till_expiration

class DealModel(QSqlQueryModel):
    success = Signal()
    error = Signal()
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.filter = None
        self.headers = ["ID", "Producto", "Oferta", "Vigencia", "Canjes Disponibles", "A", "B", "C", "D"]


    def data(self, index, role):
        value = super().data(index, Qt.DisplayRole)
        if role == Qt.DisplayRole:
            if index.column() == 2:
                if value == 0:
                    first_amount = super().data(super().index(index.row(), 3), Qt.DisplayRole)
                    second_amount = super().data(super().index(index.row(), 4), Qt.DisplayRole)
                    return f"{first_amount} x {second_amount}"
                else:
                    amount = super().data(super().index(index.row(), 5), Qt.DisplayRole)
                    price = super().data(super().index(index.row(), 6), Qt.DisplayRole)
                    return f"{amount} x {price}"
            elif index.column() == 3:
                expiration_datetime = super().data(super().index(index.row(), 7), Qt.DisplayRole)
                return get_datetime_till_expiration(expiration_datetime)
            elif index.column() == 4:
                redeems = super().data(super().index(index.row(), 8), Qt.DisplayRole)
                return redeems
            else:
                return value

    def search(self, search_str, filter):
        self.search_str = search_str
        self.filter = filter
        query = """
            SELECT deal.id, product.name, deal.type, deal.first_amount, deal.second_amount, deal.amount, deal.price, deal.expiration_date, deal.redeems FROM deal
            JOIN product ON deal.product_id = product.id
            WHERE product.{} LIKE :search_str
            ORDER BY deal.expiration_date
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

    def refresh_table(self):
        if self.filter:
            self.search(self.search_str, self.filter)
        else:
            query = """
            SELECT * FROM product_test
            ORDER BY NAME
            LIMIT 50
            """
            Qquery = QSqlQuery(query, db=self.db)
            self.setQuery(Qquery)
            self.success.emit()

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]