import sqlite3
import hashlib

from data_access import Review, check_coffee_name, create_connection, create_review, create_user, fetch_login, get_batch_id, get_best_value, get_coffee_by_description, get_most_reviews, get_roastery_id, get_unwashed

def run(connection):
    try: 
        while True:
            userId = login_register(connection)

            menu_selection(userId, connection)
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
    first_name = input()
    print("Last Name: ")
    last_name = input()

    success = create_user(connection, first_name, last_name, email, password)

    if success:
        print("Successfully Registered!")
    else:
        print(f"User with {email} already exits.")


def menu_selection(userId, connection):
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
            give_review(userId, connection)
        elif choice == 2:
            most_reviews(connection)
        elif choice == 3:
            best_value(connection)
        elif choice == 4:
            coffe_desricption(connection)
        elif choice == 5:
            unwashed(connection)
        choice = 0

# TODO importer funksjoner 
def best_value(connection):
    rows = get_best_value(connection)
    print("===== Best Score Coffees - Ordered by Best Value =====")

    for row in rows:
        print(f"Roastery Name: {row[0]}, Coffee Name: {row[1]}, Kilogram Price: {row[2]}, Average Score: {row[3]}")
    print("\n")


def most_reviews(connection):
    rows = get_most_reviews(connection)
    print("===== Most Unique Coffee Reviews =====")
    
    for row in rows:
        print(f"Name: {row[0]} {row[1]}, Unique Coffee Reviews: {row[2]}")
    print("\n")


def unwashed(connection):
    rows = get_unwashed(connection)
    for row in rows:
        print(f"Distillery: {row[0]}, Coffee Name: {row[1]}")


def give_review(userID, connection):
    review = Review(userId=userID)

    while True:
        brenneri_navn = input("Roastery Name: ")
        # TODO python renaming

        review.brenneri = get_roastery_id(connection, brenneri_navn)

        if review.brenneri is None:
            print("Error: wrong roastery name")
            continue
        break

    while True:
        review.kaffe_navn = input("Coffee Name: ")

        coffe_name_exits = check_coffee_name(connection, review.kaffe_navn)

        if not coffe_name_exits:
            print("Error: wrong coffee name")
            continue
        break

    while True:
        try:
            review.poeng = int(input("Score (0 - 10): "))
            break

        except ValueError:
            print("Wrong score: Use numbers 0 - 10")


    review.smaks_notat = input("Taste Note: ")

    review.batchId = get_batch_id(connection, review.kaffe_navn)

    create_review(connection, review)


def coffe_desricption(connection):
    # description = input("Search for coffees with description: ") 
    """Egentlig sånn det burde gjøres, men forenklet versjon nå."""

    description = "floral"

    coffees = get_coffee_by_description(connection, description)

    for coffee, roastery in coffees:
        print(coffee, roastery)

if __name__ == '__main__':
    connection = create_connection("Test.db")
    run(connection)