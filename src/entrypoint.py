import sqlite3
import hashlib

from data_access import create_user, fetch_login

def run(conn):
    
    try: 
        while True:
            userId = LoginRegister(conn)

            MenuSelection(userId, conn)
    except KeyboardInterrupt:
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
            except ValueError:
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



"""
from data_access import some_function, SomeClass

if __name__ == "__main__":
    # Kode her kjøres kun hvis man kjører denne fila direkte, altså ikke importerer den
    # tenk at all kode som skal kjøres ligger her!
    print("Hello world")
    some_function()

    c = SomeClass()
"""