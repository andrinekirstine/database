from datetime import datetime
import sqlite3
import hashlib

def create_connection(db_file):
    conn = None
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
    except sqlite3.Error as e:
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
    res = connection.execute("""SELECT c.Fornavn, c.Etternavn, count(DISTINCT a.BrentKaffeNavn) as amount FROM Kaffesmaking as a 
        INNER JOIN BrentKaffe as b ON a.BrentKaffeNavn = b.BrentKaffeNavn
        INNER JOIN Bruker as c ON a.BrukerID = c.BrukerID
        GROUP BY a.BrukerID
        ORDER BY amount DESC""")

    rows = res.fetchall()
    return rows

def get_unwashed(connection):
    res = connection.execute("""SELECT brenneri.BrenneriNavn, kaffe.BrentKaffeNavn FROM BrentKaffe as kaffe
        INNER JOIN Brenneri as brenneri ON kaffe.BrenneriID = brenneri.BrenneriID
        INNER JOIN Parti as parti ON parti.PartiID = kaffe.PartiID
        INNER JOIN Gard as gard ON gard.GardID = parti.PartiID
        WHERE parti.ForedlingNavn = 'Unwashed'
        AND (gard.Land = 'Colombia' OR gard.Land = 'Rwanda')""")
    rows = res.fetchall()
    return rows


def get_roastery_id(connection, brenneriNavn):
    res = connection.execute("Select BrenneriID FROM Brenneri WHERE BrenneriNavn = ?",  (brenneriNavn,))
    rows = res.fetchall()
    if len(rows) < 1:
        return None
    return rows[0]


def check_coffee_name(connection, kaffe_navn):
    res = connection.execute("Select count(1) FROM BrentKaffe WHERE BrentKaffeNavn = ?",  (kaffe_navn,))
    rows = res.fetchall()
    return len(rows) == 1

def get_batch_id(connection, kaffe_navn):
    res = connection.execute("Select PartiID FROM BrentKaffe WHERE BrentKaffeNavn = ?",  (kaffe_navn,))
    rows = res.fetchall()
    if len(rows) < 1:
        return None
    return rows[0]


class Review:
    def __init__(self, userId=None, poeng=None, smaks_notat=None, kaffe_navn=None, brenneri=None, batchId=None):
        self.userId = userId
        self.poeng = poeng
        self.smaks_notat = smaks_notat
        self.kaffe_navn = kaffe_navn
        self.brenneri = brenneri
        self.batchId = batchId
    def to_sql(self):
        data = [self.userId, self.poeng, self.smaks_notat, datetime.now(), self.kaffe_navn, self.brenneri, self.batchId]    
        return data


def create_review(connection, review: Review):
    data = review.to_sql()
    try:
        connection.execute("INSERT INTO Kaffesmaking(BrukerID, AntallPoeng, Smaksnotater, Dato, BrentKaffeNavn, BrenneriID, PartiID) VALUES (?,?,?,?,?,?,?)",  data)
        connection.commit()
    except Exception as e:
        print(str(e))

def get_coffee_by_description(connection, description):
    """Skal returnere liste med tupler. Kaffenavn og brenneri basert på beskrivelsen"""
    res = connection.execute("""SELECT BrentKaffeNavn, BrenneiNavn FROM BrentKaffe JOIN Brenneri on BrentKaffeNavn.BrenneriID = Brenneri.BrenneriID
        SELECT BrentKaffeNavn from Kaffesmaking where Smaksnotat like "%?%" UNION 
        SELECT BrentKaffeNavn from BrentKaffe where Beskrivelse like "%?%""",  (description,))
    rows = res.fetchall()
    if len(rows) < 1:
        return None
    return rows