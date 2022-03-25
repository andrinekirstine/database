import sqlite3
import hashlib

from data_access import create_user, fetch_login

def run(connection):
    try: 
        while True:
            userId = login_register(connection)

            MenuSelection(userId, connection)
    except KeyboardInterrupt:
        connection.close()


def login_register(connection):
    userId = None

    while userId == None:

        choice = 0
        
        while choice != 1 and choice != 2:
            try:
                print("Select option below")
                print("1. Login")
                print("2. Register")
                choice = int(input())
            except ValueError:
                print("Wrong input..")
                choice = 0
            
        if(choice == 1): #login
            userId = login(connection)
        elif(choice == 2): #register
            register(connection)

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


def register(connection):

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


def MenuSelection(userId, connection):
    # TODO endre conn til connection
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
            GiveReview(userId, connection)
        elif choice == 2:
            MostReviews(connection)
        elif choice == 3:
            BestValue(connection)
        elif choice == 4:
            GiveReview(userId, connection)
        elif choice == 5:
            Unwashed(connection)
        choice = 0


def BestValue(connection):
    rows = get_best_value(connection)
    print("===== Best Score Coffees - Ordered by Best Value =====")

    for row in rows:
        print(f"Roastery Name: {row[0]}, Coffee Name: {row[1]}, Kilogram Price: {row[2]}, Average Score: {row[3]}")
    print("\n")


def MostReviews(connection):
    rows = get_most_reviews(connection)
    print("===== Most Unique Coffee Reviews =====")
    
    for row in rows:
        print(f"Name: {row[0]} {row[1]}, Unique Coffee Reviews: {row[2]}")
    print("\n")


"""
from data_access import some_function, SomeClass

if __name__ == "__main__":
    # Kode her kjøres kun hvis man kjører denne fila direkte, altså ikke importerer den
    # tenk at all kode som skal kjøres ligger her!
    print("Hello world")
    some_function()

    c = SomeClass()
"""