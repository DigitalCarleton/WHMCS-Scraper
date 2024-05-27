import getpass
import pickle

from bs4 import BeautifulSoup

from selenium import webdriver
import selenium.webdriver.remote.webelement as webelement
from selenium.webdriver.common.by import By
# import getpass # for password input

def getDriver() -> webdriver.Chrome | webdriver.Firefox:
    # Set up the driver
    # TODO: Implement the ability to choose between Chrome and Firefox
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

def getCredentials() -> tuple[str, str]:
    use_caching = "n"
    # Get the username and password
    try:
        user = open("password.txt", "r", encoding="UTF-8").readlines()
        username = user[0].strip('\n')
        password = user[1]
    except FileNotFoundError:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")
        use_caching = input("Save your credentials for future use? (y/N): ")
    # Caching if necessary:
    if use_caching.lower() == "y":
        with open("password.txt", "w", encoding="UTF-8") as file:
            file.write(username + "\n" + password)
        
    return username, password
    

def login(driver: webdriver.Chrome | webdriver.Firefox, username: str, password: str):
    # Go to the login page
    driver.get("https://sites.carleton.edu/manage/whmcs-admin/login.php")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").submit()

def getClients(driver: webdriver.Chrome | webdriver.Firefox):
    clients = scrapeClientsPage(driver)
    for client in clients:
        updateClient(driver, client)
        print(client)
    return clients

# Scrapes the clients page of WHMCS
def scrapeClientsPage(driver: webdriver.Chrome | webdriver.Firefox) -> list[dict[str, str]]:
    driver.get("https://sites.carleton.edu/manage/whmcs-admin/clients.php")
    driver.find_elements(By.CLASS_NAME, "bootstrap-switch-label")[0].click()
    clients = []
    # Show all clients:
    hasNextPage = True
    while hasNextPage:
        clients += getFromTable(driver.find_element(By.ID, "sortabletbl0"))
        try:
            pages = driver.find_elements(By.CLASS_NAME, "page-selector")
            nextPage = pages[-1]
            print("Next page found:" + nextPage.get_attribute("href"))
            nextPage.click()
        except:
            print("No next page found")
            hasNextPage = False
    return clients

def getFromTable(table: webelement.WebElement) -> list[dict[str, str]]:
    clients = []
    soup = BeautifulSoup(table.get_attribute("outerHTML"), "html.parser")
    # Get all 'tr' elements in the table:
    rows = soup.find_all("tr")
    for row in rows:
        cells = row.find_all("td")
        if len(cells) == 9:
            client = {'id': cells[1].text,
            'firstName': cells[2].text,
            'lastName': cells[3].text,
            'company': cells[4].text,
            'email': cells[5].text,
            'numServices': int(cells[6].text.split(" ")[0]),
            'dateCreated': cells[7].text,
            'status': cells[8].text}
            clients.append(client)
    return clients        

def updateClient(driver: webdriver.Chrome | webdriver.Firefox, client: dict[str, str]):
    driver.get(f"https://sites.carleton.edu/manage/whmcs-admin/clientssummary.php?userid={client['id']}")
    # Get the client's profile page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    # TODO: Get the client's profile data
    # Get client's group
    group_parent = soup.find("td", string="Client Group").find_parent("tr")
    group = group_parent.findAll("td")[1].text
    client['group'] = group
    
    # Get client's services:
    services = []
    services_table = soup.find("th", string="Product/Service").find_parent("tr")
    rows = services_table.find_next_siblings('tr')
    for row in rows:
        cells = row.find_all("td")
        if (len(cells) == 9):
            service = {
                'id': cells[1].text,
                'domain': cells[2].text,
                'status': cells[-2].text
            }    
            services.append(service)
    client['services'] = services
    
    # Get client's admin notes
    admin_notes = soup.find("textarea", {"name": "adminnotes"}).text
    client['admin_notes'] = admin_notes 
    # TODO: Get the client's notes
    # driver.get(f"https://sites.carleton.edu/manage/whmcs-admin/clientsnotes.php?userid={client['id']}")
    # soup = BeautifulSoup(driver.page_source, "html.parser")
    return client

if __name__ == "__main__":
    username, password = getCredentials()
    driver = getDriver()
    login(driver, username, password)
    # Open the users tab and scrape the user data:
    clients = getClients(driver)
    # Save the clients to a file
    with open("clients.pkl", "wb") as file:
        pickle.dump(clients, file)