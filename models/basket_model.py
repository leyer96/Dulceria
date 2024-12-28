from PySide6.QtCore import QAbstractTableModel, Qt, Signal
from utils import Paths, get_discount, get_deal
import sqlite3

class BasketModel(QAbstractTableModel):
    success = Signal()
    total_calculated = Signal(float)
    deal_available = Signal(str)
    def __init__(self):
        super().__init__()
        self._data = []
        self.headers = ["ID", "Producto", "Marca", "Precio", "Cantidad"]
        self.total = 0
        self.discounts = []
        self.deals = []
        self.deal_added = False

    def rowCount(self,index):
        return len(self._data)
    
    def columnCount(self,index):
        return len(self.headers)
    
    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            if index.column() == 4:
                if type(value) == float:
                    return f"{value} gr."
                else:
                    return value
            return self._data[index.row()][index.column()]
        
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]
            
    def load_item(self, item_data):
        product_id = item_data[0]
        item_data_copy = item_data.copy()
        discount_data = get_discount(product_id)
        deal_data = get_deal(product_id)
        if discount_data:
            item_data[3] = discount_data["discount_price"]
            self.discounts.append({len(self._data): discount_data["redeems"]})
        if deal_data:
            type = deal_data["type"]
            amount = item_data[4]
            original_price = item_data[3]
            residue = None
            if type == 0:
                first_amount = deal_data["first_amount"]
                second_amount = deal_data["second_amount"]
                if amount >= first_amount:
                    n = int(amount / first_amount)
                    residue = amount - n*first_amount 
                    original_price = item_data[3]
                    new_price = second_amount * original_price
                    item_data[1] = f"{item_data[1]} {first_amount} x {second_amount}"
                    item_data[3] = new_price
                    item_data[4] = n
                    self.deals.append({len(self._data): deal_data["redeems"]})
                    self._data.append(item_data)
                    self.deal_added = True
                else:
                    self.deal_available.emit(f"{first_amount} x {second_amount}")
            else:
                deal_amount = deal_data["amount"]
                deal_price = deal_data["deal_price"]
                if amount >= deal_amount:
                    n_deal = int(amount / deal_amount)
                    residue = amount - n_deal * deal_amount
                    new_price = deal_price * n_deal
                    item_data[1] = f"{item_data[1]} {deal_amount} x {deal_price}"
                    item_data[3] = new_price
                    item_data[4] = n_deal
                    self.deals.append({len(self._data): deal_data["redeems"]})
                    self._data.append(item_data)
                    self.deal_added = True
                else:
                    self.deal_available.emit(f"{deal_amount} x ${deal_price}")     
        if not self.deal_added:
            self._data.append(item_data)
        else:
            if residue:
                print(item_data_copy)
                item_data_copy[4] = residue
                self._data.append(item_data_copy)
            self.deal_added = False
        self.calculate_total()
        self.layoutChanged.emit()

    def calculate_total(self):
        total = 0
        for item in self._data:
            total += item[3]*item[4]
        self.total = total
        self.total_calculated.emit(total)

    def reset_basket(self):
        self._data = []
        self.discounts = []
        self.total_calculated.emit(0)
        self.success.emit()
        