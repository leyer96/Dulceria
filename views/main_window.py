from PySide6.QtWidgets import QMainWindow, QStackedLayout, QWidget
from views.home.home_window import HomeWindow
from views.menu_widget import Menu
from views.products.products_window import ProductsWindow
from views.payments.payments_window import PaymentsWindow
from views.stock.stock_window import StockWindow
from views.admin.admin_window import AdminWindow
from views.deals.deals_window import DealsWindow

class MainWindow(QMainWindow):
    def __init__(self, db):
        super().__init__()

        # self.resize(700, 500)
 
        windows = [HomeWindow, ProductsWindow, PaymentsWindow, StockWindow, DealsWindow, AdminWindow]
        initialized_window = []

        container = QWidget()
        container_layout = QStackedLayout()

        for window in windows:
            menu = Menu()
            menu.go_to_home.connect(lambda: container_layout.setCurrentIndex(0))
            menu.go_to_products.connect(lambda: container_layout.setCurrentIndex(1))
            menu.go_to_payments.connect(lambda: container_layout.setCurrentIndex(2))
            menu.go_to_stock.connect(lambda: container_layout.setCurrentIndex(3))
            menu.go_to_deals.connect(lambda: container_layout.setCurrentIndex(4))
            menu.go_to_admin.connect(lambda: container_layout.setCurrentIndex(5))
            w = window(db, menu)

            initialized_window.append(w)
            container_layout.addWidget(w)

        for i in range(0, len(initialized_window)):
            for j in range(0,len(initialized_window)):
                if i == j:
                    continue
                wi = initialized_window[i]
                wj = initialized_window[j]
                if isinstance(wi, HomeWindow):
                    if isinstance(wj, DealsWindow):
                        wi.checkout.payment_saved.connect(wj.deal_model.refresh_table)
                        wi.checkout.payment_saved.connect(wj.discount_model.refresh_table)
                    elif isinstance(wj, PaymentsWindow):
                        wi.checkout.payment_saved.connect(wj.model.get_todays_payment)
                    elif isinstance(wj, StockWindow):
                        wi.checkout.payment_saved.connect(wj.stock_model.refresh_table)
                elif isinstance(wi, StockWindow):
                    if isinstance(wj, DealsWindow):
                        wi.discount_added.connect(wj.discount_model.refresh_table)
                        wi.discount_added.connect(lambda: print("DISCOUNT ADDED"))
                        wi.deal_added.connect(wj.deal_model.refresh_table)
                        wi.deal_added.connect(lambda: print("DEAL ADDED"))
                    # wj.menu.go_to_stock.connect(wi.stock_model.get_all_stock)
                    # wj.menu.go_to_stock.connect(wi.batch_model.get_all_batchs)
                elif isinstance(wi, AdminWindow):
                    wi.new_settings.connect(wj.load_settings)
                    wj.menu.go_to_admin.connect(wi.hide_content)
                elif isinstance(wi, ProductsWindow):
                    if isinstance(wj, HomeWindow):
                        wi.product_created.connect(wj.search_box.model.refresh_table)
                        wi.product_edited.connect(wj.search_box.model.refresh_table)
                    if isinstance(wj, StockWindow):
                        wi.model.product_deleted.connect(wj.stock_model.refresh_table)
                        wi.model.product_deleted.connect(wj.batch_model.refresh_table)
                        wi.product_created.connect(wj.stock_model.refresh_table)
                        wi.product_edited.connect(wj.stock_model.refresh_table)
                        wi.product_edited.connect(wj.batch_model.refresh_table)
                    elif isinstance(wj, DealsWindow):
                        wi.model.product_deleted.connect(wj.deal_model.refresh_table)
                        wi.model.product_deleted.connect(wj.discount_model.refresh_table)
                        wi.product_edited.connect(wj.discount_model.refresh_table)
                        wi.product_edited.connect(wj.deal_model.refresh_table)

        container.setLayout(container_layout)
        
        self.setCentralWidget(container)
        self.show()
        # self.showFullScreen()