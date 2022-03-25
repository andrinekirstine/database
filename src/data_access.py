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


def create_user(connection, firstName, lastName, email, password):
    data = (firstName, lastName, email, password)
    try:
        connection.execute("INSERT INTO Bruker(Fornavn, Etternavn, Epostadresse, Passord) VALUES (?,?,?,?)",  data)
        connection.commit()
    except ValueError:
        return False
    return True


def get_best_value(connection):
    res = connection.execute("""SELECT b.BrenneriNavn, a.BrentKaffeNavn, c.KiloprisKr,  SUM(a.AntallPoeng) * 1.0 / COUNT(a.AntallPoeng) as poeng 
        FROM Kaffesmaking a 
        INNER JOIN BrentKaffe c ON a.BrentKaffeNavn = c.BrentKaffeNavn 
        INNER JOIN Brenneri b ON a.BrenneriID = b.BrenneriID 
        GROUP BY a.BrentKaffeNavn 
        ORDER BY (poeng / KiloprisKr) DESC""")
    rows = res.fetchall()
    return rows


def get_most_reviews(connection):
    res = conn.execute("""SELECT c.Fornavn, c.Etternavn, count(DISTINCT a.BrentKaffeNavn) as amount FROM Kaffesmaking as a 
        INNER JOIN BrentKaffe as b ON a.BrentKaffeNavn = b.BrentKaffeNavn
        INNER JOIN Bruker as c ON a.BrukerID = c.BrukerID
        GROUP BY a.BrukerID
        ORDER BY amount DESC""")

    rows = res.fetchall()
    return rows



"""
def some_function():
    print("Hello from some module")

class SomeClass:
    def __init__(self):
        print("Hello from some class")
"""