import mysql.connector

DBCONFIG = {'host': 'eu-cdbr-west-02.cleardb.net',
            'user': 'b8a14ff118d075',
            'password': '0922b736',
            'database': 'heroku_b7354dfae7a5454'}


class MySQLDatabase:
    conn = mysql.connector.connect(**DBCONFIG)
    cursor = conn.cursor()
