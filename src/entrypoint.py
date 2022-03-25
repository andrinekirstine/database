import sqlite3
import hashlib

def run(conn):
    
    try: 
        while True:
            userId = LoginRegister(conn)

            MenuSelection(userId, conn)
    except KeyboardInterrupt:
        conn.close()





"""
from data_access import some_function, SomeClass

if __name__ == "__main__":
    # Kode her kjøres kun hvis man kjører denne fila direkte, altså ikke importerer den
    # tenk at all kode som skal kjøres ligger her!
    print("Hello world")
    some_function()

    c = SomeClass()
"""