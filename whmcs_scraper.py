import time
from tables import *
import connection as conn

from bs4 import BeautifulSoup

from selenium import webdriver
import selenium.webdriver.remote.webelement as webelement
from selenium.webdriver.common.by import By

def getClients(driver: webdriver.Chrome | webdriver.Firefox):
    clients = scrapeClientsPage(driver)
    #! For testing purposes, only update the first 4 clients
    for client in clients[:4]:
        updateClient(driver, client)
    return clients

# Scrapes the clients page of WHMCS
def scrapeClientsPage(driver: webdriver.Chrome | webdriver.Firefox) -> list[dict[str, str]]:
    driver.get("https://sites.carleton.edu/manage/whmcs-admin/clients.php")
    driver.find_elements(By.CLASS_NAME, "bootstrap-switch-label")[0].click()
    clients = []
    # Show all clients:
    hasNextPage = True
    while hasNextPage:
        clients += clientFromTable(driver.find_element(By.ID, "sortabletbl0"))
        try:
            pages = driver.find_elements(By.CLASS_NAME, "page-selector")
            nextPage = pages[-1]
            print("Next page found:" + nextPage.get_attribute("href"))
            nextPage.click()
        except:
            print("No next page found")
            hasNextPage = False
    return clients       

def updateClient(driver: webdriver.Chrome | webdriver.Firefox, client: dict[str, str]):
    driver.get(f"https://sites.carleton.edu/manage/whmcs-admin/clientssummary.php?userid={client['id']}")
    # Get the client's profile page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # Get client's group
    group_parent = soup.find("td", string="Client Group").find_parent("tr")
    group = group_parent.findAll("td")[1].text
    client['group'] = group
    # Get client's services
    services_table = soup.find("th", string="Product/Service").find_parent("tr")
    client['services'] = servicesFromTable(services_table)
    # Get client's admin notes
    admin_notes = soup.find("textarea", {"name": "adminnotes"}).text
    client['adminNotes'] = admin_notes 
    # Get client's notes
    driver.get(f"https://sites.carleton.edu/manage/whmcs-admin/clientsnotes.php?userid={client['id']}")
    soup = BeautifulSoup(driver.page_source, "html.parser")
    notes_table = soup.find("table", {"id": "sortabletbl1"})
    client['notes'] = notesFromTable(notes_table)
    return client

# TODO: Do we make one entry per service, or do we make one entry per client?
def writeFile(filename: str, clients: list[dict[str, str]]):
    f = open(filename, "w")
    # Headers:
    keys = ["id", "firstName", "lastName", "email", "status", "group", "adminNotes", "numServices", "services", "notes"]
    f.write(",".join(keys) + "\n")
    # Body:
    for client in clients:
        print(client)
        line = []
        for key in keys:
            if key in client:
                line.append(str(client[key]))
            else:
                line.append("")
        f.write(",".join(line) + "\n")
    
    
    f.close()

if __name__ == "__main__":
    username, password = conn.getCredentials()
    driver = conn.getDriver()
    conn.login(driver, username, password)
    # Open the users tab and scrape the user data:
    
    # #! TEMP: DELETE
    # import pickle
    # try:
    #     clients = pickle.load(open("clients.pkl", "rb"))
    # except: 
    #     clients = getClients(driver)
    #     with open("clients.pkl", "wb") as f:
    #         pickle.dump(clients, f)
    # #! ^ TEMP: DELETE
    clients = getClients(driver)
    
    # Write the data to a file:
    now = time.localtime()
    filename = f"clients_{now.tm_year}_{now.tm_mon}_{now.tm_mday}.csv"
    writeFile(filename, clients)        