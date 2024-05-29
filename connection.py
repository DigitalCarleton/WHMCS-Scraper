from selenium import webdriver
from selenium.webdriver.common.by import By
import getpass

def getDriver() -> webdriver.Chrome | webdriver.Firefox:
    # Set up the driver
    # TODO: Implement the ability to choose between Chrome and Firefox
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

def getCredentials() -> tuple[str, str]:
    # Get the username and password
    try:
        user = open("password.txt", "r", encoding="UTF-8").readlines()
        username = user[0].strip('\n')
        password = user[1]
    except FileNotFoundError:
        username = input("Enter your username: ")
        password = getpass.getpass("Enter your password: ")        
    return username, password
    

def login(driver: webdriver.Chrome | webdriver.Firefox, username: str, password: str):
    # Go to the login page
    driver.get("https://sites.carleton.edu/manage/whmcs-admin/login.php")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").submit()