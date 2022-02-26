from database import MySQLDatabase


class Stock:
    def __init__(self, price='', item=''):
        self.price = price.rstrip()
        self.item = item.rstrip()


class Shop(MySQLDatabase):

    def check_if_item_exists(self, product: Stock):
        self.cursor.execute(f"select * from shop where item = '{product.item}' and price = '{product.price}'")
        return bool(self.cursor.fetchall())

    def add_new_item(self, product: Stock):
        self.cursor.execute(f"INSERT INTO shop (item, price) values ('{product.item}', '{product.price}')")
        self.conn.commit()
