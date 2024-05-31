import time
from helpers.tables import *
from helpers.write_file import writeFile
from tqdm import tqdm

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By

def getClients(driver: webdriver.Chrome | webdriver.Firefox):
    print("Scraping 'clients' page...")
    clients = scrapeClientsPage(driver)
    print("Updating clients...")
    for client in tqdm(clients):
        updateClient(driver, client)
    return clients

# Scrapes the clients page of WHMCS
def scrapeClientsPage(driver: webdriver.Chrome | webdriver.Firefox) -> list[dict[str, str]]:
    driver.get("https://sites.carleton.edu/manage/whmcs-admin/clients.php")
    driver.find_elements(By.CLASS_NAME, "bootstrap-switch-label")[0].click()
    clients = []
    
    lastPage = int(driver.find_elements(By.CLASS_NAME, "page-selector")[-2].text)
    for i in range(0, int(lastPage)):
        print(f"scraping page {i+1}/{lastPage}")
        clients += clientFromTable(driver.find_element(By.ID, "sortabletbl0"))
        
        driver.find_elements(By.CLASS_NAME, "page-selector")[-1].click()
    
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