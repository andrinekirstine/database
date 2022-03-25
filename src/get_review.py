from datetime import datetime

import sqlite3
import hashlib
from sqlite3 import Error
from time import timezone
conn = None

def create_connection(db_file):
    conn = None
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def run(conn):
    while True:
        userId = LoginRegister(conn)

        MenuSelection(userId, conn)

    conn.close()


def LoginRegister(connection):
    userId = None

    while userId == None:

        choice = 0
        
        while choice != 1 and choice != 2:
            try:
                print("Select option below")
                print("1. Login")
                print("2. Register")
                choice = int(input())
            except:
                print("Wrong input..")
                choice = 0
            
        if(choice == 1): #login
            userId = login(connection)
        elif(choice == 2): #register
            Register(connection)

    return userId

def login(connection):
    print("===== Login =====")
    print("Email: ")
    email = input()
    print("password: ")
    password = hashlib.sha256(input().encode()).hexdigest()

    rows = fetch_login(connection, email, password)

    if len(rows) <= 0:
        print(f"Error: Incorrect Email or Password")
        return None
    else:
        print(f"Successfully logged in with UserID {rows[0][0]}")
        return rows[0][0]

def fetch_login(connection, email, password):
    res = connection.execute("Select * FROM Bruker WHERE Epostadresse = ? AND Passord = ?",  (email, password))
    rows = res.fetchall()
    return rows

def Register(connection):
    print("===== Register =====")
    print("Email: ")
    email = input()
    print("Password: ")
    password = hashlib.sha256(input().encode()).hexdigest()
    print(password)
    print("First Name: ")
    firstName = input()
    print("Last Name: ")
    lastName = input()

    success = create_user(connection, firstName, lastName, email, password)

    if success:
        print("Successfully Registered!")
    else:
        print(f"User with {email} already exits.")


def create_user(connection, firstName, lastName, email, password):
    data = (firstName, lastName, email, password)
    try:
        connection.execute("INSERT INTO Bruker(Fornavn, Etternavn, Epostadresse, Passord) VALUES (?,?,?,?)",  data)
        connection.commit()
    except ValueError:
        return False
    return True

def MenuSelection(userId, conn):
    choice = 0
    while choice != 6:
        while choice < 1 or choice > 6:
            try:
                print("Select option below")
                print("1. Give Review") # Done
                print("2. List of most unique coffee reviewers") # Done
                print("3. Best Value Coffee") # Done
                print("4. Search for \"Floral\"")
                print("5. Unwashed Coffee from Rwanda and Colombia") # Done
                print("6. Logout") # Done
                choice = int(input())
            except ValueError:
                print("Wrong input..")
                print("\n")
                choice = 0
    
        if choice == 1:
            GiveReview(userId, conn)
        elif choice == 2:
            MostReviews(conn)
        elif choice == 3:
            BestValue(conn)
        elif choice == 4:
            GiveReview(userId, conn)
        elif choice == 5:
            Unwashed(conn)
        choice = 0
        
def get_best_value(connection):
    res = connection.execute("""SELECT b.BrenneriNavn, a.BrentKaffeNavn, c.KiloprisKr,  SUM(a.AntallPoeng) * 1.0 / COUNT(a.AntallPoeng) as poeng 
        FROM Kaffesmaking a 
        INNER JOIN BrentKaffe c ON a.BrentKaffeNavn = c.BrentKaffeNavn 
        INNER JOIN Brenneri b ON a.BrenneriID = b.BrenneriID 
        GROUP BY a.BrentKaffeNavn 
        ORDER BY (poeng / KiloprisKr) DESC""")
    rows = res.fetchall()
    return rows

def BestValue(connection):
    rows = get_best_value(connection)
    print("===== Best Score Coffees - Ordered by Best Value =====")

    for row in rows:
        print(f"Roastery Name: {row[0]}, Coffee Name: {row[1]}, Kilogram Price: {row[2]}, Average Score: {row[3]}")
    print("\n")

def get_most_reviews(connection):
    res = conn.execute("""SELECT c.Fornavn, c.Etternavn, count(DISTINCT a.BrentKaffeNavn) as amount FROM Kaffesmaking as a 
        INNER JOIN BrentKaffe as b ON a.BrentKaffeNavn = b.BrentKaffeNavn
        INNER JOIN Bruker as c ON a.BrukerID = c.BrukerID
        GROUP BY a.BrukerID
        ORDER BY amount DESC""")

    rows = res.fetchall()
    return rows

def MostReviews(connection):
    rows = get_most_reviews(connection)
    print("===== Most Unique Coffee Reviews =====")
    
    for row in rows:
        print(f"Name: {row[0]} {row[1]}, Unique Coffee Reviews: {row[2]}")
    print("\n")

def Unwashed(conn):
    res = conn.execute("""SELECT brenneri.BrenneriNavn, kaffe.BrentKaffeNavn FROM BrentKaffe as kaffe
        INNER JOIN Brenneri as brenneri ON kaffe.BrenneriID = brenneri.BrenneriID
        INNER JOIN Parti as parti ON parti.PartiID = kaffe.PartiID
        INNER JOIN Gard as gard ON gard.GardID = parti.PartiID
        WHERE parti.ForedlingNavn = 'Unwashed'
        AND (gard.Land = 'Colombia' OR gard.Land = 'Rwanda')""")
    rows = res.fetchall()
    for row in rows:
        print(f"Distillery: {row[0]}, Coffee Name: {row[1]}")

def GiveReview(userId, conn):
    keepGoing = True

    brenneri = None
    kaffeNavn = ""
    poeng = 0

    while keepGoing == True:
        print("Distillery Name: ")
        brenneriNavn = input()

        res = conn.execute("Select * FROM Brenneri WHERE BrenneriNavn = ?",  [brenneriNavn])

        brenneriRows = res.fetchall()
        if len(brenneriRows) < 1:
            print("Error: wrong dystillery name")
            continue
        
        brenneri = brenneriRows[0]

        break

    while keepGoing == True:
        print("Coffee Name: ")
        kaffeNavn = input()

        res = conn.execute("Select * FROM BrentKaffe WHERE BrentKaffeNavn = ?",  [kaffeNavn])

        rows = res.fetchall()
        if len(rows) < 1:
            print("Error: wrong coffee name")
            continue
        break

    while keepGoing == True:
        print("Score (0 - 10): ")
        try:
            poeng = int(input()) # add try catch
            break
        except:
            print("Wrong score: Use numbers 0 - 10")


    print("Taste Note: ")
    smaksNotat = input()

    print("Batch ID: ")
    batchId = int(input())

    data = [userId, poeng, smaksNotat, datetime.now(), kaffeNavn, brenneri[0], batchId]
    try:
        conn.execute("INSERT INTO Kaffesmaking(BrukerID, AntallPoeng, Smaksnotater, Dato, BrentKaffeNavn, BrenneriID, PartiID) VALUES (?,?,?,?,?,?,?)",  data)
        conn.commit()
    except Exception as e:
        print(str(e))

if __name__ == '__main__':
    conn = create_connection("Test.db")
    run(conn)
