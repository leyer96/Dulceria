import os
class Paths:
    base = os.path.dirname(__file__)
    data = os.path.join(base, "data")
    icons = os.path.join(base, "resources/icons")  
    models = os.path.join(base, "models")
    settings = os.path.join(base, "settings")
    style = os.path.join(base, "resources/styles.qss")
    threads = os.path.join(base, "models/threads")
    views = os.path.join(base, "views")
    tests = os.path.join(base, "TEST")
    
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
    @classmethod
    def test(cls, filename):
        return os.path.join(cls.tests, filename)
    
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
    con = sqlite3.connect(Paths.test("db.db"))
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE,
                brand VARCHAR(50),
                price FLOAT NOT NULL,
                category VARCHAR(20) NOT NULL,
                code TEXT UNIQUE
                )
                """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                payment_form TEXT NOT NULL,
                amount FLOAT NOT NULL,
                note TEXT
            );
                """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS productpayment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                payment_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                amount INTEGER NOT NULL,
                unit_price FLOAT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES product(id)
                FOREIGN KEY (payment_id) REFERENCES payment(id)
            );
                """)
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                amount INT DEFAULT 0,
                status INT DEFAULT 1,
                FOREIGN KEY (product_id) REFERENCES product(id)
                )
                """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS batch (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                stock_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                amount INT NOT NULL,
                expiration_date DATE,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                show INTEGER DEFAULT 1,
                FOREIGN KEY (product_id) REFERENCES product(id)
                FOREIGN KEY (stock_id) REFERENCES stock(id)
                )
                """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS discount (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER UNIQUE,
                price FLOAT NOT NULL,
                expiration_date DATETIME,
                redeems INTEGER,
                FOREIGN KEY (product_id) REFERENCES product(id)
                )
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS deal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER UNIQUE,
                type INTEGER DEFAULT 0,
                first_amount INTEGER,
                second_amount INTEGER,
                amount INTEGER,
                price FLOAT,
                expiration_date DATETIME,
                redeems INTEGER,
                FOREIGN KEY (product_id) REFERENCES product(id)
                )
        """)
def create_db_tables():
    con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS product (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(100) NOT NULL UNIQUE,
                brand VARCHAR(50),
                price FLOAT NOT NULL,
                category VARCHAR(20) NOT NULL,
                code TEXT UNIQUE
                )
                """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS payment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                payment_form TEXT NOT NULL,
                amount FLOAT NOT NULL,
                note TEXT
            );
                """)
    
    cur.execute("""
        CREATE TABLE IF NOT EXISTS productpayment (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                payment_id INTEGER NOT NULL,
                product_name TEXT NOT NULL,
                amount INTEGER NOT NULL,
                unit_price FLOAT NOT NULL,
                FOREIGN KEY (product_id) REFERENCES product(id)
                FOREIGN KEY (payment_id) REFERENCES payment(id)
            );
                """)
    cur.execute(""" 
        CREATE TABLE IF NOT EXISTS stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                amount INT DEFAULT 0,
                status INT DEFAULT 1,
                FOREIGN KEY (product_id) REFERENCES product(id)
                )
                """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS batch (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                stock_id INTEGER NOT NULL,
                product TEXT NOT NULL,
                amount INT NOT NULL,
                expiration_date DATE,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                show INTEGER DEFAULT 1,
                FOREIGN KEY (product_id) REFERENCES produt(id)
                FOREIGN KEY (stock_id) REFERENCES stock(id)
                )
                """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS discount (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER UNIQUE
                price FLOAT NOT NULL
                expiration_date DATETIME
                redeems INTEGER
                FOREIGN KEY (product_id) REFERENCES product(id)
                )
        """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS deal (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER UNIQUE,
                type INTEGER DEFAULT 0,
                first_amount INTEGER,
                second_amount INTEGER,
                amount INTEGER,
                price FLOAT,
                expiration_date DATETIME,
                redeems INTEGER,
                FOREIGN KEY (product_id) REFERENCES product(id)
                )
        """)
    
def drop_test_tables():
    con = sqlite3.connect(Paths.test("db.db"))
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS payment")
    cur.execute("DROP TABLE IF EXISTS productpayment")
    cur.execute("DROP TABLE IF EXISTS product")
    cur.execute("DROP TABLE IF EXISTS stock")
    cur.execute("DROP TABLE IF EXISTS batch")

def drop_db_tables():
    con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    cur.execute("DROP TABLE IF EXISTS payment")
    cur.execute("DROP TABLE IF EXISTS productpayment")
    cur.execute("DROP TABLE IF EXISTS product")
    cur.execute("DROP TABLE IF EXISTS stock")
    cur.execute("DROP TABLE IF EXISTS batch")


def save_payment(payment_data, products):
    con = sqlite3.connect(Paths.test("db.db"))
    # con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    payment_form = payment_data["payment_form"]
    amount = payment_data["amount"]
    note = payment_data["note"]
    timestamp = datetime.now()
    try:
        cur.execute("""
            INSERT INTO payment (payment_form, amount, note, timestamp) VALUES(?,?,?,?)
                    """,(payment_form, amount, note, timestamp))
    except sqlite3.Error as e:
        print(e)
        return False
    else:
        payment_id = cur.lastrowid
        for product in products:
            print("SAVING PRODCUT")
            print(product)
            product_id = int(product[0])
            product_name = product[1]
            unit_price = float(product[3])
            amount = int(product[4])
            try:
                cur.execute("""
                    INSERT INTO productpayment (product_id, payment_id, product_name, amount, unit_price) VALUES(?,?,?,?,?)
                        """,(product_id, payment_id, product_name, amount, unit_price))
            except:
                return False
            else:
                con.commit()
        return True
    
def get_all_from_productpayment():
    con = sqlite3.connect(Paths.test("db.db"))
    # con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    data = cur.execute(""" 
        SELECT * FROM productpayment
        JOIN payment ON productpayment.payment_id = payment.id
    """).fetchall()
    return data

def get_prodcutpayment_from_payment_id(payment_id):
    con = sqlite3.connect(Paths.test("db.db"))
    # con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    data = cur.execute(""" 
        SELECT * FROM productpayment
        JOIN payment ON productpayment.payment_id = payment.id
        WHERE payment.id = ?
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
    con = sqlite3.connect(Paths.test("db.db"))
    # con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    data = cur.execute(""" 
        SELECT * FROM productpayment
        JOIN payment ON productpayment.payment_id = payment.id
        WHERE payment.timestamp BETWEEN ? AND ?;
    """, (date_start_str, date_end_str)).fetchall()
    return data

def get_discount(product_id):
    con = sqlite3.connect(Paths.test("db.db"))
    # con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    discount = cur.execute("SELECT * FROM discount WHERE product_id = ?", (product_id,)).fetchone()
    if discount:
        discount_price = discount[2]
        expiration_date_str = discount[3]
        expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d %H:%M:%S.%f")
        redeems = discount[4]
        if expiration_date < datetime.now():
            try:
                cur.execute("DELETE FROM discuont WHERE product_id = ?", (product_id,))
            except sqlite3.Error as e:
                print(e)
            else:
                con.commit()
            finally:
                return False
        else:
            discount_data = {
                "discount_price": discount_price,
                "redeems": redeems
            }
            return discount_data
    else:
        return False
    
def get_deal(product_id):
    con = sqlite3.connect(Paths.test("db.db"))
    # con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    discount = cur.execute("SELECT * FROM deal WHERE product_id = ?", (product_id,)).fetchone()
    if discount:
        type = discount[2]
        expiration_date_str = discount[7]
        expiration_date = datetime.strptime(expiration_date_str, "%Y-%m-%d %H:%M:%S.%f")
        redeems = discount[8]
        if expiration_date < datetime.now():
            try:
                cur.execute("DELETE FROM discuont WHERE product_id = ?", (product_id,))
            except sqlite3.Error as e:
                print(e)
            else:
                con.commit()
            finally:
                return False
        else:
            if type == 0:
                first_amount = discount[3]
                second_amount = discount[4]
                deal_data = {
                    "type": type,
                    "first_amount": first_amount,
                    "second_amount": second_amount,
                    "redeems": redeems
                }
            else:
                amount = discount[5]
                deal_price = discount[6]
                deal_data = {
                    "type": type,
                    "amount": amount,
                    "deal_price": deal_price,
                    "redeems": redeems
                }
            return deal_data
    else:
        return False

def substract_from_stock(products, deals_0, deals_1):
    con = sqlite3.connect(Paths.test("db.db"))
    # con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    try:
        for product in products:
            product_id = product[0]
            name = product[1]
            amount = product[4]
            prev_amount = cur.execute("SELECT amount FROM stock WHERE stock.product_id = ?", (product_id,)).fetchone()[0]
            if product_id in deals_0 or product_id in deals_1:
                og_name = cur.execute("SELECT name FROM product WHERE id = ?", (product_id,)).fetchone()[0]
                if name != og_name:
                    if product_id in deals_0:
                        times = cur.execute("SELECT first_amount FROM deal WHERE product_id = ?", (product_id,)).fetchone()[0]
                        amount = amount * times
                    else:
                        times = cur.execute("SELECT amount FROM deal WHERE product_id = ?", (product_id,)).fetchone()[0]
                        amount = amount * times
            if prev_amount > 0:
                new_amount = max(0, int(prev_amount - amount))
                cur.execute("UPDATE stock SET amount = ? WHERE stock.product_id = ?", (new_amount, product_id))
            else:
                print("ERROR DE EMPAREJAMIENTO CON STOCK REAL")
                return False
    except sqlite3.Error as e:
        print(e)
        return False
    else:
        con.commit()
        return True

def update_discount(products, discounts):
    con = sqlite3.connect(Paths.test("db.db"))
    # con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    if not discounts:
        return True
    try:
        for product in products:
            product_id = product[0]
            if product_id in discounts:
                redeems = product[4]
                available_redeems = cur.execute("SELECT redeems FROM discount WHERE product_id = ?", (product_id,)).fetchone()[0]
                new_available_redeems = available_redeems - redeems
                if new_available_redeems <= 0:
                    print("REDEEMS EXPIRED")
                    cur.execute("DELETE FROM discount WHERE product_id = ?", (product_id,))
                else:
                    print("REEDEMS UPDATING")
                    cur.execute("UPDATE discount SET redeems = ? WHERE product_id = ?", (new_available_redeems, product_id))
    except sqlite3.Error as e:
        print(e)
        return False
    else:
        con.commit()
        return True

def update_deal(products, deals):
    if not deals:
        return True
    con = sqlite3.connect(Paths.test("db.db"))
    # con = sqlite3.connect(Paths.db())
    cur = con.cursor()
    try:
        for product in products:
            product_id = product[0]
            name = product[1].lower()
            if product_id in deals:
                og_name = cur.execute("SELECT name FROM product WHERE id = ?", (product_id,)).fetchone()[0]
                print(f"OG NAME: {og_name} AND BOUGHT: {name}")
                if name != og_name:
                    print(f"UPDATING FOR {name}")
                    redeems = product[4]
                    available_redeems = cur.execute("SELECT redeems FROM deal WHERE product_id = ?", (product_id,)).fetchone()[0]
                    new_available_redeems = available_redeems - redeems
                    if new_available_redeems <= 0:
                        print("REDEEMS EXPIRED")
                        cur.execute("DELETE FROM deal WHERE product_id = ?", (product_id,))
                    else:
                        print("REEDEMS UPDATING")
                        cur.execute("UPDATE deal SET redeems = ? WHERE product_id = ?", (new_available_redeems, product_id))
    except sqlite3.Error as e:
        print(e)
        return False
    else:
        con.commit()
        return True

def get_expiration_date(days):
    today = datetime.today()
    expiration_date = today + timedelta(days=days)
    return expiration_date


import csv
def create_csv_file(data, headers, folder_path, filename):
    path = folder_path + "/" + filename +  ".csv"
    with open(path, "w") as f:
        writer = csv.writer(f)
        field = headers
        writer.writerow(field)
        for row in data:
            writer.writerow(row)

def get_datetime_till_expiration(exp_date_str):
    expiration_date_obj = datetime.strptime(exp_date_str, datetime_raw_format)
    delta = expiration_date_obj - datetime.now()
    delta_days = delta.days
    delta_seconds = delta.seconds
    delta_hours = int(delta_seconds / 3600)
    if delta_hours:
        dt_str = f"{delta_days} días {delta_hours} horas"
    else:
        dt_str = f"{delta_days} días"
    if expiration_date_obj < datetime.now():
        return "VENCIDO"
    return dt_str

def get_days_till_expiration(exp_date_str):
    if exp_date_str == no_exipration_date_date:
        return "SIN CADUCIDAD"
    expiration_date_obj = datetime.strptime(exp_date_str, date_raw_format)
    delta = expiration_date_obj - datetime.today()
    delta_days = delta.days
    if delta_days < 0:
        return "CADUCADO"
    return delta_days

# SETTINGS
import json
def load_settings():
    with open(Paths.setting("settings.json"), "r") as f:
        data = json.load(f)
        return data
def save_settings(settings):
    with open(Paths.setting("settings.json"), "w") as f:
        dump = json.dumps(settings)
        try:
            f.write(dump)
        except Exception as e:
            print(e)
            return False
        else:
            f.close()
            return True

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

product_categories = [
    default_cb_str,
    "Dulce",
    "Chocolate",
    "Papas",
    "Decoración",
    "Fiesta",
    "Desechable",
    "Vestir"
]

date_raw_format = "%Y-%m-%d"
datetime_raw_format = "%Y-%m-%d %H:%M:%S.%f"
date_format = "%d-%m-%Y"
no_exipration_date_date = "2111-11-11"



    

    