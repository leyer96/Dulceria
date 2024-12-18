from PySide6.QtCore import QAbstractTableModel, Qt, Signal

class BasketModel(QAbstractTableModel):
    total_calculated = Signal(float)
    def __init__(self):
        super().__init__()
        self._data = []
        self.headers = ["ID", "Producto", "Marca", "Precio", "Cantidad"]
        self.total = 0

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
        self._data.append(item_data)
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
        self.total_calculated.emit(0)
        