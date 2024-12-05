import os

class Paths:
    base = os.path.dirname(__file__)
    data = os.path.join(base, "data")
    icons = os.path.join(base, "resources/icons")  
    models = os.path.join(base, "models")
    settings = os.path.join(base, "config")
    style = os.path.join(base, "resources/styles.qss")
    threads = os.path.join(base, "models/threads")
    views = os.path.join(base, "views")
    
    # File loaders
    @classmethod
    def db(cls):
        return os.path.join(cls.data, "db.db")
    @classmethod
    def icon(cls, filename):
        return os.path.join(cls.icons, filename)
    @classmethod
    def image(cls, filename):
        return os.path.join(cls.images, filename)
    @classmethod
    def model(cls, filename):
        return os.path.join(cls.models, filename)
    @classmethod
    def setting(cls, filename):
        return os.path.join(cls.settings, filename)
    @classmethod
    def thread(cls, filename):
        return os.path.join(cls.settings, filename)
    @classmethod
    def view(cls, filename):
        return os.path.join(cls.views, filename)
    
def toggle_btns_state(btns):
    for btn in btns:
        if btn.isEnabled():
            btn.setEnabled(False)
        else:
            btn.setEnabled(True)

import sqlite3
def create_test_tables():
    con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payment_test (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                payment_form TEXT NOT NULL,
                amount FLOAT NOT NULL,
                note TEXT
            );
                """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS productpayment_test (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                payment_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                amount INTEGER NOT NULL,
                unit_price FLOAT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES product_test(id)
                FOREIGN KEY (payment_id) REFERENCES payment_test(id)
            );
                """)
    
def drop_test_tables():
    con = sqlite3.connect(Paths.db())
    cur = con.cursor()

    cur.execute("DROP TABLE payment_test")
    cur.execute("DROP TABLE productpayment_test")

def save_payment(payment_data, products):
    print("PASSED PRODUCTS")
    print(products)
    con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    payment_form = payment_data["payment_form"]
    amount = payment_data["amount"]
    note = payment_data["note"]
    try:
        cur.execute("""
            INSERT INTO payment_test (payment_form, amount, note) VALUES(?,?,?)
                    """,(payment_form, amount, note))
        con.commit()
    except:
        return False
    else:
        payment_id = cur.lastrowid

        for product in products:
            print("SAVING PRODUT")
            print(product)
            product_id = int(product[0])
            product_name = product[1]
            unit_price = float(product[2])
            amount = int(product[3])
            try:
                cur.execute("""
                    INSERT INTO productpayment_test (product_id, payment_id, product_name, amount, unit_price) VALUES(?,?,?,?,?)
                        """,(product_id, payment_id, product_name, amount, unit_price))
                con.commit()
            except:
                return False
        return True


    

    