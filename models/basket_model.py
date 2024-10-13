from PySide6.QtCore import QAbstractTableModel, Qt, Signal

class BasketModel(QAbstractTableModel):
    total = Signal(float)
    def __init__(self):
        super().__init__()
        self._data = []
        self.headers = ["ID", "Producto", "Precio", "Cantidad"]

    def rowCount(self,index):
        return len(self._data)
    
    def columnCount(self,index):
        return 4
    
    def data(self, index, role):
        if role == Qt.DisplayRole:
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
            total += item[3]*int(item[2])
        self.total.emit(total)
        