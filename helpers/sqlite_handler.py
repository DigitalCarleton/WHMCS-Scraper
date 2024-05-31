# Building an SQLite database for our clients' data:

import sqlite3
from sqlite3 import Connection
from sqlite3.dbapi2 import Cursor

def createClientsTable(conn: Connection):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS clients;")
    c.execute('''CREATE TABLE clients
                 (id INTEGER PRIMARY KEY, 
                 firstName TEXT, 
                 lastName TEXT, 
                 email TEXT, 
                 status TEXT, 
                 groupName TEXT, 
                 adminNotes TEXT, 
                 numServices INTEGER, 
                 notes TEXT);''')
    conn.commit()
    c.close()
    
def createServicesTable(conn: Connection):
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS services;")
    c.execute('''CREATE TABLE services
                 (id INTEGER PRIMARY KEY, 
                 clientId INTEGER, 
                 domain TEXT, 
                 status TEXT);''')
    conn.commit()
    c.close()    

def insertClient(conn: Connection, client: dict[str, str]) -> bool:
    cur = conn.cursor()
    cur.execute(f" SELECT * FROM clients WHERE id = {client['id']}" )
    if cur.fetchone() is not None:
        return False
    
    cur.execute(f""" INSERT INTO clients
                    (id, firstName, lastName, email, status, groupName, adminNotes, numServices, notes)
                    VALUES
                    ({client['id']}, 
                    '{client['firstName']}', 
                    '{client['lastName']}', 
                    '{client['email']}', 
                    '{client['status']}', 
                    '{client['group']}', 
                    '{client['adminNotes']}', 
                    {client['numServices']}, 
                    '{client['notes']}')
                """)
    
#! 'clientID' may need to be passed in as a parameter
def insertService(conn: Connection, s: dict[str, str]) -> bool:
    cur = conn.cursor()
    cur.execute(f" SELECT * FROM services WHERE id = {s['id']}" )
    if cur.fetchone() is not None:
        return False
    
    cur.execute(f""" INSERT INTO services
                    (id, clientId, domain, status)
                    VALUES
                    ({s['id']}, 
                    {s['clientId']}, 
                    '{s['domain']}', 
                    '{s['status']}')
                """)
    conn.commit()
    cur.close()
    return True

if __name__ == "__main__":
    conn = sqlite3.connect('whmcs_clients.db')
    reset = input("Reset the database? (y/N): ")
    if reset.lower() == 'y':
        createClientsTable(conn)
        createServicesTable(conn)
    conn.close()