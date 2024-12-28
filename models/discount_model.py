from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Signal, Qt
from utils import get_datetime_till_expiration

class DiscountModel(QSqlQueryModel):
    success = Signal()
    error = Signal()
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.filter = None
        self.headers = ["ID", "Producto", "Precio", "Vigencia", "Canjes Disponibles"]

    def data(self, index, role):
        value = super().data(index, Qt.DisplayRole)
        if role == Qt.DisplayRole:
            if index.column() == 3:
                expiration_datetime = value
                return get_datetime_till_expiration(expiration_datetime)
            else:
                return value

    def search(self, search_str, filter):
        self.search_str = search_str
        self.filter = filter
        query = """
            SELECT discount.id, product.name, discount.price, discount.expiration_date, discount.redeems FROM discount
            JOIN product ON  discount.product_id = product.id
            WHERE product.{} LIKE :search_str
            ORDER BY discount.expiration_date
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

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]