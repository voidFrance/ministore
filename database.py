# database.py
import mysql.connector


def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='ministore',
        password='123mudar',
        database='ministore'
    )
