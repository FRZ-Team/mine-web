from hashlib import md5

import mysql.connector.errors

from database import MySQLDatabase

DBCONFIG = {'host': 'eu-cdbr-west-02.cleardb.net',
            'user': 'b8a14ff118d075',
            'password': '0922b736',
            'database': 'heroku_b7354dfae7a5454'}


class User:
    def __init__(self, username='', password='', email='', ip='', root=''):
        self.username = username.rstrip()
        self.password = md5(password.encode('utf-8')).hexdigest().rstrip()
        self.email = email.rstrip()
        self.ip = ip.rstrip()
        self.root = root.rstrip()


class UsersTable(MySQLDatabase):

    def __init__(self):
        self.conn = mysql.connector.connect(**DBCONFIG)
        self.cursor = self.conn.cursor()

    def check_if_user_exist(self, user: User):
        try:
            self.cursor.execute(
                f"SELECT * FROM users WHERE username = '{user.username}' AND password = '{user.password}'")
            return bool(self.cursor.fetchall())

        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.OperationalError):
            self.conn()
            self.cursor.execute(
                f"SELECT * FROM users WHERE username = '{user.username}' AND password = '{user.password}'")
            return bool(self.cursor.fetchall())

    def add_new_user(self, user: User):
        try:
            # check if user already exist
            self.cursor.execute(f"SELECT * FROM users WHERE username = '{user.username}'")
            # return error if user already exist
            if self.cursor.fetchall():
                return 'username already exists'
            # register if it is a new user
            else:
                self.cursor.execute(f"""insert into users (username, password, email, ip)
                                        values 
                                        ('{user.username}', '{user.password}', '{user.email}', '{user.ip}')""")

                self.conn.commit()
                return 'user successfully added'

        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.OperationalError):
            self.conn()
            self.cursor.execute(f"SELECT * FROM users WHERE username = '{user.username}'")
            if self.cursor.fetchall():
                return 'username already exists'
            else:
                self.cursor.execute(f"""insert into users (username, password, email, ip)
                                                   values 
                                                   ('{user.username}', '{user.password}', '{user.email}', '{user.ip}')""")

                self.conn.commit()
                return 'user successfully added'

    def send_request_to_change_users_password(self, user: User):
        try:
            self.cursor.execute(f"select * from users where username = '{user.username}' and email = '{user.email}'")
            return bool(self.cursor.fetchall())

        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.OperationalError):
            self.conn()
            self.cursor.execute(f"select * from users where username = '{user.username}' and email = '{user.email}'")
            return bool(self.cursor.fetchall())

    def change_users_password(self, user: User):
        try:
            self.cursor.execute(f"UPDATE users SET password = '{user.password}' WHERE username = '{user.username}'")
            self.conn.commit()
            return True

        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.OperationalError):
            self.conn()
            self.cursor.execute(f"UPDATE users SET password = '{user.password}' WHERE username = '{user.username}'")
            self.conn.commit()
            return True

    def registration_date(self, user: User):
        try:
            self.cursor.execute(f"select registration from users where username = '{user.username}'")
            for row in self.cursor.fetchall():
                return row[0]

        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.OperationalError):
            self.conn()
            self.cursor.execute(f"select registration from users where username = '{user.username}'")
            for row in self.cursor.fetchall():
                return row[0]

    def update_last_login_date(self, user: User):
        try:
            self.cursor.execute(f"UPDATE users SET lastLogin = CURRENT_TIMESTAMP WHERE username = '{user.username}'")
            self.conn.commit()

        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.OperationalError):
            self.conn()
            self.cursor.execute(f"UPDATE users SET lastLogin = CURRENT_TIMESTAMP WHERE username = '{user.username}'")
            self.conn.commit()

    def last_login_date(self, user: User):
        try:
            self.cursor.execute(f"SELECT lastLogin FROM users WHERE username = '{user.username}'")
            for row in self.cursor.fetchall():
                return row[0]

        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.OperationalError):
            self.conn()
            self.cursor.execute(f"SELECT lastLogin FROM users WHERE username = '{user.username}'")
            for row in self.cursor.fetchall():
                return row[0]

    def set_roots(self, user: User):
        try:
            self.cursor.execute(f"""UPDATE users SET roots = '{user.root}' WHERE username = '{user.username}'""")
        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.OperationalError):
            self.conn()
            self.cursor.execute(f"""UPDATE users SET roots = '{user.root}' WHERE username = '{user.username}'""")

    def show_roots(self, user: User):
        try:
            self.cursor.execute(f"SELECT roots FROM users WHERE username = '{user.username}'")
            for row in self.cursor.fetchall():
                return row[0]

        except (mysql.connector.errors.InterfaceError, mysql.connector.errors.OperationalError):
            self.conn()
            self.cursor.execute(f"SELECT roots FROM users WHERE username = '{user.username}'")
            for row in self.cursor.fetchall():
                return row[0]
