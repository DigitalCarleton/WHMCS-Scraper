# Building an SQLite database for our clients' data:

import sqlite3
from sqlite3 import Connection
from sqlite3.dbapi2 import Cursor
from tqdm import tqdm

def writeClientsToDB(clients: list[dict[str, str]]):
    conn = sqlite3.connect('whmcs_clients.db')
    reset = input("Reset the database? (y/N): ")
    if reset.lower() == 'y':
        createClientsTable(conn)
        createServicesTable(conn)
     
    print("Inserting clients into database...")
    for client in tqdm(clients):
        insertClient(conn, client)        
        for service in client['services']:
            insertService(conn, client['id'], service)    
    conn.close()

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
    for key in client.keys():
        if type(client[key]) == str:
            client[key] = client[key].replace("'", "`")
    cur = conn.cursor()
   
    if checkForClientChange(conn, client): 
        cur.execute(f"""INSERT INTO clients
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
        conn.commit()
        cur.close()
    
def checkForClientChange(conn: Connection, client: dict[str, str]) -> bool:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM clients WHERE id = {client['id']}")
    db_client = cur.fetchone()
    if (db_client is None) or (len(client.keys()) < 9):
        return True

    keys = ['id', 'firstName', 'lastName', 'email', 'status', 'group', 'adminNotes', 'numServices']
    for i in range(1, len(keys)):
        if db_client[i] != client[keys[i]]:
            print(f"\nAltering client {client['id']} : {db_client[i]} != {client[keys[i]]}")
            cur.execute(f"""DELETE FROM clients WHERE id = {client['id']}""")
            conn.commit()
            cur.close()
            return True
    return False
    
def insertService(conn: Connection, clientID, s: dict[str, str]) -> bool:
    cur = conn.cursor()    
    s['clientID'] = clientID
    if checkForServiceChange(conn, s):
        cur.execute(f"""INSERT INTO services
                        (id, clientId, domain, status)
                        VALUES
                        ({s['id']}, 
                        {clientID}, 
                        '{s['domain']}', 
                        '{s['status']}')
                    """)
    conn.commit()
    cur.close()
    return True

def checkForServiceChange(conn: Connection, s: dict[str, str]) -> bool:
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM services WHERE id = {s['id']}")
    db_service = cur.fetchone()
    if db_service is None:
        return True

    keys = [('id', int), ('clientID', int), ('domain', str), ('status', str)]
    for i in range(1, len(keys)):
        t = keys[i][1]
        if db_service[i] != t(s[keys[i][0]]):
            print(f"\nAltering service {s['id']} : {db_service[i]} != {s[keys[i][0]]}")
            cur.execute(f"""DELETE FROM services WHERE id = {s['id']}""")
            conn.commit()
            cur.close()
            return True
    return False