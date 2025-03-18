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
        self.deals_0 = []
        self.deals_1 = []
        self.deal_added = False

    def rowCount(self,index):
        return len(self._data)
    
    def columnCount(self,index):
        return len(self.headers)
    
    def data(self, index, role):
        if role == Qt.DisplayRole:
            value = self._data[index.row()][index.column()]
            col = index.column()
            if col == 3:
                value = str(value) + " $"
            elif col == 4:
                if type(value) == float:
                    return f"{value} gr."
                else:
                    return value
            return value
        
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.headers[section]
            
    def load_item(self, basket_item):
        basket_item[3] = float(basket_item[3].split("$")[0].strip())
        item_grouped = self.group_equals(basket_item)
        if item_grouped is not False:
            # CASE: ITEM IN BASKET
            self.apply_deal_to_active(item_grouped)
        else:
            # CASE: ITEM NOT IN BASKET
            basket_items = self.apply_deal(basket_item)
            if len(basket_items) == 2:
                # CASE: AMOUNT > DEAL AMOUNT
                basket_item = basket_items[0]
                deal_basket_item = basket_items[1]
                item_grouped = self.group_equals(deal_basket_item)
                if item_grouped is False:
                    # CASE: DEAL NOT IN BASKET
                    self._data.append(basket_item)
                    self._data.append(deal_basket_item)
                else:
                    # CASE: DEAL WAS IN BASKET
                    self._data.append(basket_item)
            else:
                # CASE: AMOUNT <= DEAL AMOUNT
                basket_item = basket_items[0]
                # CASE: DEAL WAS IN BASKET
                item_grouped = self.group_equals(basket_item)
                if item_grouped is False:
                    # CASE: DEAL WAS NOT IN BASKET
                    self._data.append(basket_item)
        self.calculate_total()
        self.layoutChanged.emit()

    def group_equals(self, basket_item):
        if len(self._data) > 0:
            product = basket_item[1]
            active_products = [product[1] for product in self._data]
            if product in active_products:
                item_index = active_products.index(product)
                new_amount = basket_item[4]
                prev_amount = self._data[item_index][4]
                self._data[item_index][4] = prev_amount + new_amount
                return item_index
            else:
                return False
        else:
            return False
    
    def apply_deal_to_active(self, item_index):
        active_item = self._data[item_index]
        active_item_copy = active_item.copy()
        basket_items = self.apply_deal(active_item_copy, False)
        if len(basket_items) == 2:
            # CASE: ITEM AMOUNT > DEAL AMOUNT
            deal_basket_item = basket_items[0]
            product_basket_item = basket_items[1]
            self._data[item_index][4] = product_basket_item[4]
            # CASE: DEAL IN BASKET
            deal_grouped = self.group_equals(deal_basket_item)
            if deal_grouped is False:
                # CASE: DEAL NOT IN BASKET
                self._data.append(basket_items[0])
        else:
            # CASE ITEM AMOUNT <= DEAL AMOUNT
            basket_item = basket_items[0]
            if basket_item[1] != active_item[1]:
                # CASE: ITEM AMOUNT == DEAL AMOUNT
                del(self._data[item_index])
                # CASE: DEAL IN BASKET
                item_grouped = self.group_equals(basket_item)
                if item_grouped is False:
                    # CASE: DEAL NOT IN BASKET
                    self._data.append(basket_item)
            else:
                # CASE: AMOUNT < DEAL AMOUNT
                pass
    
    def apply_deal(self, basket_item, show_message=True):
        product_id = basket_item[0]
        bakset_item_copy = basket_item.copy()
        discount_data = get_discount(product_id)
        deal_data = get_deal(product_id)
        residue = 0
        basket_items = []
        # DISCOUNT
        if discount_data:
            basket_item[3] = discount_data["discount_price"]
            basket_items.append(basket_item)
            if product_id not in self.discounts:
                print("ID ADDED TO DISCOUNTS")
                self.discounts.append(product_id)
        # DEAL
        elif deal_data:
            type = deal_data["type"]
            amount = basket_item[4]
            original_price = basket_item[3]
            residue = 0
            if type == 0:
                first_amount = deal_data["first_amount"]
                second_amount = deal_data["second_amount"]
                if amount >= first_amount:
                    n_deal_redeems = int(amount / first_amount)
                    residue = amount - n_deal_redeems*first_amount 
                    new_price = second_amount * original_price
                    basket_item[1] = f"{basket_item[1]} ({first_amount} x {second_amount})"
                    basket_item[3] = new_price
                    basket_item[4] = n_deal_redeems
                    if product_id not in self.deals_0:
                        self.deals_0.append(product_id)
                    basket_items.append(basket_item)
                else:
                    basket_items.append(basket_item)
                    if show_message:
                        self.deal_available.emit(f"{first_amount} x {second_amount}")
            else:
                deal_amount = deal_data["amount"]
                deal_price = deal_data["deal_price"]
                if amount >= deal_amount:
                    n_deal_redeems = int(amount / deal_amount)
                    residue = amount - n_deal_redeems * deal_amount
                    basket_item[1] = f"{basket_item[1]} ({deal_amount} x ${deal_price})"
                    basket_item[3] = deal_price
                    basket_item[4] = n_deal_redeems
                    if product_id not in self.deals_1:
                        self.deals_1.append(product_id)
                    basket_items.append(basket_item)
                else:
                    basket_items.append(basket_item)
                    if show_message:
                        self.deal_available.emit(f"{deal_amount} x ${deal_price}")
            if residue:
                    bakset_item_copy[4] = residue
                    basket_items.append(bakset_item_copy)
        else:
            basket_items.append(basket_item)
        return basket_items

    def calculate_total(self):
        total = 0
        for item in self._data:
            price = item[3]
            amount = item[4]
            total += price*amount
        self.total = total
        self.total_calculated.emit(total)

    def reset_basket(self):
        self._data = []
        self.discounts = []
        self.deals_0 = []
        self.deals_1 = []
        self.total_calculated.emit(0)
        self.success.emit()
    
    def delete_item(self, row):
        if row != None:
            del(self._data[row])
            self.calculate_total()
            self.layoutChanged.emit()
        