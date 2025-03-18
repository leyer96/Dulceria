from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt, Signal

class StockModel(QSqlQueryModel):
    error = Signal()
    success = Signal()
    no_record = Signal()
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.headers = ["ID", "Producto", "Marca", "Categoría", "Cantidad en Stock"]
        self.filter = None
    
    def data(self, index, role):
        value = super().data(index, Qt.DisplayRole)
        if role == Qt.DisplayRole:
            if index.column() == 1 or index.column() == 2:
                    return value.capitalize()
            return value
    def search(self, search_str, filter, show_msg=True):
        self.search_str = search_str
        self.filter = filter
        query = """
            SELECT product.id, product.name, product.brand, product.category, stock.amount FROM stock
            JOIN product ON stock.product_id = product.id
            WHERE product.{} LIKE :search_str
            ORDER BY stock.amount
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

    def get_all_stock(self):
        query = """
            SELECT product.id, product.name, product.brand, product.category, stock.amount FROM stock
            JOIN product ON stock.product_id = product.id
            ORDER BY stock.amount
            LIMIT 50
        """
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)
        self.success.emit()

    def refresh_table(self):
        if self.filter:
            self.search(self.search_str, self.filter, show_msg=False)
        else:
            self.get_all_stock()

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]
