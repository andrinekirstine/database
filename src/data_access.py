import sqlite3
import hashlib

def create_connection(db_file):
    conn = None
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def fetch_login(connection, email, password):
    res = connection.execute("Select * FROM Bruker WHERE Epostadresse = ? AND Passord = ?",  (email, password))
    rows = res.fetchall()
    return rows





"""
def some_function():
    print("Hello from some module")

class SomeClass:
    def __init__(self):
        print("Hello from some class")
"""