from PySide6.QtSql import QSqlQueryModel, QSqlQuery
from PySide6.QtCore import Qt, Signal

class StockModel(QSqlQueryModel):
    error = Signal()
    success = Signal()
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
    def search(self, search_str, filter):
        self.search_str = search_str
        self.filter = filter
        query = """
            SELECT product_test.id, product_test.name, product_test.brand, product_test.category, stock_test.amount FROM stock_test
            JOIN product_test ON stock_test.product_id = product_test.id
            WHERE product_test.{} LIKE :search_str
            ORDER BY stock_test.amount
            LIMIT 50
        """.format(filter)
        Qquery = QSqlQuery(db=self.db)
        Qquery.prepare(query)
        Qquery.bindValue(":search_str", f"%{search_str}%")
        if not Qquery.exec():
            self.error.emit()
        else:
            self.setQuery(Qquery)

    def get_all_stock(self):
        query = """
            SELECT product_test.id, product_test.name, product_test.brand, product_test.category, stock_test.amount FROM stock_test
            JOIN product_test ON stock_test.product_id = product_test.id
            ORDER BY stock_test.amount
            LIMIT 50
        """
        Qquery = QSqlQuery(query, db=self.db)
        self.setQuery(Qquery)

    def refresh_table(self):
        if self.filter:
            query = """
            SELECT product_test.id, product_test.name, product_test.brand, product_test.category, stock_test.amount FROM stock_test
            JOIN product_test ON stock_test.product_id = product_test.id
            WHERE product_test.{} LIKE :search_str
            ORDER BY stock_test.amount
            LIMIT 50
        """.format(self.filter)
            Qquery = QSqlQuery(db=self.db)
            Qquery.prepare(query)
            Qquery.bindValue(":search_str", f"%{self.search_str}%")
            if not Qquery.exec():
                self.error.emit()
            else:
                self.setQuery(Qquery)
        else:
            self.get_all_stock()

    def headerData(self, section, orientation, role):
           if role == Qt.DisplayRole:
               if orientation == Qt.Horizontal:
                   return self.headers[section]
