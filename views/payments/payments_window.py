from PySide6.QtWidgets import (
    QWidget,
    QTableView,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QAbstractItemView,
    QHeaderView,
    QVBoxLayout,
    QFileDialog,
    QMessageBox,
    QSpacerItem
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtGui import QIcon
from datetime import datetime
from views.payments.search_widget import SearchWidget
from views.dialogs.view_payment_details import ViewPaymentDetailsDialog
from views.dialogs.select_export_data import SelectExportDataDialog
from models.payment_model import PaymentModel
from utils import (
    Paths, 
    create_csv_file, 
    get_all_from_productpayment,
    get_prodcutpayment_from_payment_id,
    get_prodcutpayment_from_month,
    load_settings
    )
class PaymentsWindow(QWidget):
      def __init__(self, db, menu):
            super().__init__()

            self.db = db
            self.menu = menu
            self.search_widget = SearchWidget()
            self.table = QTableView()
            self.model = PaymentModel(db)
            title = QLabel("Pagos")
            self.view_details_btn = QPushButton(QIcon(Paths.icon("application-detail.png")),"Ver Detalles")
            self.export_data_btn = QPushButton(QIcon(Paths.icon("document-excel-csv.png")),"Exportar Datos")
            self.cash_amount_label = QLabel()
            self.card_amount_label = QLabel()

            btns_layout = QHBoxLayout()
            btns_layout.addWidget(self.view_details_btn)
            btns_layout.addWidget(self.export_data_btn)
            # CONFIG
            self.table.setModel(self.model)
            self.selected_row = -1
            self.table.clicked.connect(self.on_clicked_row)
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            self.table.setSelectionMode(QAbstractItemView.SingleSelection)
            self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
            self.menu.go_to_payments_btn.setEnabled(False)
            self.view_details_btn.setEnabled(False)
            title.setStyleSheet("font-size: 30px; font-weight: bold")   
            # SIGNALS
            self.search_widget.data.connect(lambda date_data: self.model.search(date_data))
            self.view_details_btn.clicked.connect(self.open_payment_details_dialog)
            self.export_data_btn.clicked.connect(self.open_select_export_data_dialog)
            self.model.success.connect(self.calculate_amount)
            self.model.success.connect(lambda: self.view_details_btn.setEnabled(False))
            self.model.error.connect(lambda: self.view_details_btn.setEnabled(False))
            self.model.no_record.connect(lambda: QMessageBox.information(self, "Sin Resultados", "No se registraron pagos entre las fechas seleccionadas"))

            self.filler = QWidget()

            # LOGO
            logo_label = QLabel()
            logo_pixmap = QPixmap(Paths.image("dulceria_logo.png")).scaledToWidth(100)
            logo_label.setPixmap(logo_pixmap)
            
            # LAYOUT
            self.cash_label = QLabel("Efectivo: ")
            self.card_label = QLabel("Tarjeta: ")

            cash_amount_layout = QHBoxLayout()
            cash_amount_layout.addWidget(self.cash_label)
            cash_amount_layout.addWidget(self.cash_amount_label)
            card_amount_layout = QHBoxLayout()
            card_amount_layout.addWidget(self.card_label)
            card_amount_layout.addWidget(self.card_amount_label)

            layout = QHBoxLayout()

            left_layout = QVBoxLayout()
            left_layout.addWidget(title)
            left_layout.addWidget(self.search_widget)
            left_layout.addWidget(self.table)
            left_layout.addLayout(btns_layout)

            right_layout = QVBoxLayout()
            right_layout.addWidget(logo_label)
            right_layout.addWidget(self.menu)
            right_layout.addLayout(cash_amount_layout)
            right_layout.addLayout(card_amount_layout)
            right_layout.insertSpacing(0, 30)
            right_layout.addStretch()
            right_layout.setAlignment(self.menu, Qt.AlignTop)
            right_layout.setAlignment(logo_label,Qt.AlignHCenter | Qt.AlignTop)

            layout.addLayout(left_layout)
            layout.addLayout(right_layout)

            layout.setStretch(0, 4)
            layout.setStretch(1, 1)
            
            self.setLayout(layout)

            self.model.get_todays_payment()
            self.load_settings()

      def on_clicked_row(self, index):
            self.selected_row = index.row()
            if not self.view_details_btn.isEnabled():
                  self.view_details_btn.setEnabled(True)

      def open_payment_details_dialog(self):
            row = self.selected_row
            if row > -1:
                  payment_id = self.model.data(self.model.index(row, 0), Qt.DisplayRole)
                  payment_timestamp = self.model.data(self.model.index(row, 1), Qt.DisplayRole)
                  payment_form = self.model.data(self.model.index(row, 2), Qt.DisplayRole)
                  amount = self.model.data(self.model.index(row, 3), Qt.DisplayRole)
                  note = self.model.data(self.model.index(row, 4), Qt.DisplayRole)
                  payment_data = {
                        "id": payment_id,
                        "timestamp": payment_timestamp,
                        "payment_form": payment_form,
                        "amount": amount,
                        "note": note
                  }
                  dlg = ViewPaymentDetailsDialog(payment_data)
                  dlg.exec()
            
      def to_default(self):
            self.model.get_todays_payment()
            self.search_widget.to_default()

      def open_select_export_data_dialog(self):
            is_query = False
            if self.model.rowCount() > 0:
                  is_query = True
            dlg = SelectExportDataDialog(is_query)
            dlg.option_selected.connect(self.export_data)
            dlg.exec()

      def export_data(self, option):
            # SELECT FOLDER
            today_str = datetime.today().strftime("%d-%m-%Y")
            if option == "curr":
                  data = []
                  for r in range(0, self.model.rowCount()):
                        payment_id = self.model.data(self.model.index(r,0), Qt.DisplayRole)
                        productpayments = get_prodcutpayment_from_payment_id(payment_id)
                        for productpayment in productpayments:
                              data.append(productpayment)
                        fn = "extracto-del-" + today_str
            elif option == "all":
                  data = get_all_from_productpayment()
                  fn = "todos-pagos-" + today_str
            else:
                  month = option
                  data = get_prodcutpayment_from_month(month)
                  fn = "datos-" + month
            if len(data) > 0:
                  dirname = QFileDialog.getExistingDirectory(self, "Seleccionar Folder")
                  if dirname:
                        formated_data = []
                        for entry in data:
                              print(len(entry))
                              timestamp = entry[7]
                              dateandtime = timestamp.split(" ")
                              payment_id = entry[2]
                              payment_form = entry[8]
                              product = entry[3]
                              amount = entry[4]
                              price = entry[5]
                              data = [payment_id, *dateandtime, product, price, amount, payment_form]
                              formated_data.append(data)
                        headers = ["ID_PAGO", "FECHA", "HORA", "PRODUCTO", "PRECIO UNITARIO", "CANTIDAD", "FORMAD DE PAGO"]
                        create_csv_file(formated_data, headers, dirname, fn)
            else:
                  QMessageBox.information(self, "Estatus", "No hay datos que exportar con los parámetros seleccionados.")
      
      def load_settings(self):
            pass

      def calculate_amount(self):
            rows = self.model.rowCount()
            cash = 0
            card = 0
            for i in range(0, rows):
                  type = self.model.data(self.model.index(i, 2), Qt.DisplayRole)
                  amount = float(self.model.data(self.model.index(i, 3), Qt.DisplayRole)[1:])
                  if type == "Efectivo":
                        cash += amount
                  else:
                        card += amount
            self.cash_amount_label.setText(f"${str(cash)}")
            self.card_amount_label.setText(f"${str(card)}")
              

                  