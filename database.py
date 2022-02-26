import mysql.connector
from hashlib import md5

DBCONFIG = {'host': '127.0.0.1',
            'user': 'root',
            'password': 'Uruk-hai_berserk1',
            'database': 'mcgriefdb'}


class User:
    def __init__(self, username='', password='', email='', ip='', root=''):
        self.username = username.rstrip()
        self.password = md5(password.encode('utf-8')).hexdigest().rstrip()
        self.email = email.rstrip()
        self.ip = ip.rstrip()
        self.root = root.rstrip()


class MySQLDatabase:
    conn = mysql.connector.connect(**DBCONFIG)
    cursor = conn.cursor()

    def check_if_user_exist(self, user: User):
        self.cursor.execute(f"SELECT * FROM users WHERE username = '{user.username}' AND password = '{user.password}'")
        return bool(self.cursor.fetchall())

    def add_new_user(self, user: User):
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

    def send_request_to_change_users_password(self, user: User):
        self.cursor.execute(f"select * from users where username = '{user.username}' and email = '{user.email}'")
        return bool(self.cursor.fetchall())

    def change_users_password(self, user: User):
        self.cursor.execute(f"UPDATE users SET password = '{user.password}' WHERE username = '{user.username}'")
        self.conn.commit()
        return True

    def registration_date(self, user: User):
        self.cursor.execute(f"select registration from users where username = '{user.username}'")
        for row in self.cursor.fetchall():
            return row[0]

    def update_last_login_date(self, user: User):
        self.cursor.execute(f"UPDATE users SET lastLogin = CURRENT_TIMESTAMP WHERE username = '{user.username}'")
        self.conn.commit()

    def last_login_date(self, user: User):
        self.cursor.execute(f"SELECT lastLogin FROM users WHERE username = '{user.username}'")
        for row in self.cursor.fetchall():
            return row[0]


class Root(MySQLDatabase):

    def set_roots(self, user: User):
        self.cursor.execute(f"""UPDATE users SET roots = '{user.root}' WHERE username = '{user.username}'""")

    def show_roots(self, user: User):
        self.cursor.execute(f"SELECT roots FROM users WHERE username = '{user.username}'")
        for row in self.cursor.fetchall():
            return row[0]
