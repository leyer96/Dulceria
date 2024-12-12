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
    
# GUI
def toggle_btns_state(btns):
    for btn in btns:
        if btn.isEnabled():
            btn.setEnabled(False)
        else:
            btn.setEnabled(True)

# DB
import sqlite3
def create_test_tables():
    con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product_test (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                price FLOAT NOT NULL,
                category TEXT NOT NULL,
                code TEXT
                )
                """)
    
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
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS stock_test (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                amount INT DEFAULT 0,
                status INT DEFAULT 1,
                FOREIGN KEY (product_id) REFERENCES product_test(id)
                )
                """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS batch_test (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                stock_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                amount INT NOT NULL,
                expiration_date DATE,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                show INTEGER DEFAULT 1,
                FOREIGN KEY (product_id) REFERENCES produt_test(id)
                FOREIGN KEY (stock_id) REFERENCES stock(id)
                )
                """)
    
def drop_test_tables():
    con = sqlite3.connect(Paths.db())
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS payment_test")
    cur.execute("DROP TABLE IF EXISTS productpayment_test")
    cur.execute("DROP TABLE IF EXISTS product_test")
    cur.execute("DROP TABLE IF EXISTS stock_test")
    cur.execute("DROP TABLE IF EXISTS batch_test")


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
    
def get_all_from_productpayment():
    con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    data = cur.execute(""" 
        SELECT * FROM productpayment_test
        JOIN payment_test ON productpayment_test.payment_id = payment_test.id
    """).fetchall()
    return data

def get_prodcutpayment_from_payment_id(payment_id):
    con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    data = cur.execute(""" 
        SELECT * FROM productpayment_test
        JOIN payment_test ON productpayment_test.payment_id = payment_test.id
        WHERE payment_test.id = ?
    """, (payment_id,)).fetchall()
    return data

from datetime import datetime, timedelta
def get_prodcutpayment_from_month(month):
    month = months.index(month) + 1
    curr_date = datetime.today()
    year = curr_date.year
    date_start = datetime(day=1, month=month, year = year)
    if month == 12:
        month = 1
        year = year + 1
    date_end = datetime(year=year, month=month+1, day=1) - timedelta(days=1)
    date_start_str = date_start.strftime("%Y-%m-%d")
    date_end_str = date_end.strftime("%Y-%m-%d")
    con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    data = cur.execute(""" 
        SELECT * FROM productpayment_test
        JOIN payment_test ON productpayment_test.payment_id = payment_test.id
        WHERE payment_test.timestamp BETWEEN ? AND ?;
    """, (date_start_str, date_end_str)).fetchall()
    return data

def substract_from_stock(products):
    con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    for product in products:
        product_id = product[0]
        amount = product[3]
        prev_amount = cur.execute("SELECT amount from stock_test where stock_test.product_id = ?", (product_id,)).fetchone()[0]
        if prev_amount > 0:
            new_amount = prev_amount - amount
            cur.execute("UPDATE stock_test SET amount = ? WHERE stock_test.product_id = ?", (new_amount, product_id))
        else:
            print("ERROR DE EMPAREJAMIENTO CON STOCK REAL")
    con.commit()
    return True

import csv
def create_csv_file(data, headers, folder_path, filename):
    path = folder_path + "/" + filename +  ".csv"
    with open(path, "w") as f:
        writer = csv.writer(f)
        field = headers
        writer.writerow(field)
        for row in data:
            writer.writerow(row)

# GLOBAL
default_cb_str = "--SELECCIONAR--"
months = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre"
    ]



    

    