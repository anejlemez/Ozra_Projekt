import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="127.0.0.1",       
        user="root",
        password="ozrageslo",
        port=3307,
        database="mydb"
    )