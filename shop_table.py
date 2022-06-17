from database import MySQLDatabase

import mysql.connector.errors

import os

DBCONFIG = os.environ.get("DBCONFIG")


class Stock:
    def __init__(self, price='', item=''):
        self.price = price.rstrip()
        self.item = item.rstrip()


class Shop(MySQLDatabase):

    def __init__(self):
        self.conn = mysql.connector.connect(**DBCONFIG)
        self.cursor = self.conn.cursor()

    def check_if_item_exists(self, product: Stock):
        try:
            self.cursor.execute(f"select * from shop where item = '{product.item}' and price = '{product.price}'")
            return bool(self.cursor.fetchall())

        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.OperationalError):
            self.conn()
            self.cursor.execute(f"select * from shop where item = '{product.item}' and price = '{product.price}'")
            return bool(self.cursor.fetchall())

    def add_new_item(self, product: Stock):
        try:
            self.cursor.execute(f"INSERT INTO shop (item, price) values ('{product.item}', '{product.price}')")
            self.conn.commit()

        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.OperationalError):
            self.conn()
            self.cursor.execute(f"INSERT INTO shop (item, price) values ('{product.item}', '{product.price}')")
            self.conn.commit()
