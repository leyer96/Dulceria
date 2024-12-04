import sqlite3
from utils import Paths

def create_test_table():
    con = sqlite3.connect(Paths.data("db.db"))
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS product_test(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            price FLOAT NOT NULL,
            code INT UNIQUE
            )
        """)
    test_values = [
        ("PALETA", 10, None),
        ("PAPAS", 30, None),
        ("CHOCOLATE", 30, None),
        ("GOMITAS", 20, None)
    ]
    cur.executemany("""
        INSERT INTO product_test (name, price, code) VALUES(?,?,?)
    """, test_values)
    con.commit()

create_test_table()