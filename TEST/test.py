import sqlite3
# from utils import Paths

con = sqlite3.connect("../data/db.db")
cur = con.cursor()

query = """
            SELECT product_test.id, product_test.name, product_test.brand, product_test.category, stock_test.amount FROM stock_test
            JOIN product_test ON stock_test.product_id = product_test.id
            WHERE product_test.name LIKE '%{}%'
            ORDER BY stock_test.amount
            LIMIT 50
        """.format("a")

r = cur.execute(query).fetchall()
print(r)