import time
from helpers.tables import *
from helpers.write_file import writeFile
import helpers.connection as conn
from helpers.whmcs_scraper import getClients
from helpers.sqlite_handler import writeClientsToDB

def main():
    username, password = conn.getCredentials()
    driver = conn.getDriver()
    conn.login(driver, username, password)
    # Open the users tab and scrape the user data:
    clients = getClients(driver)
    
    #! For debugging purposes, we can unpickle an example set:
    # import pickle
    # clients = pickle.load(open("clients.pkl", "rb"))
    
    # Write the data to a database:
    writeClientsToDB(clients)
    # Write the data to a file:
    now = time.localtime()
    filename = f"WHMCS_clients_{now.tm_year}_{now.tm_mon}_{now.tm_mday}.csv"
    writeFile(filename, clients) 

if __name__ == "__main__":
    main()