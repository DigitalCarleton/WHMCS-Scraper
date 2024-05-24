import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# import getpass # for password input

def getDriver() -> webdriver.Chrome | webdriver.Firefox:
    # Set up the driver
    # TODO: Implement the ability to choose between Chrome and Firefox
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

def getCredentials() -> tuple[str, str]:
    # Get the username and password
    try:
        user = open("password.txt", "r").readlines()
        username = user[0].strip('\n')
        password = user[1].strip('\n')
    except FileNotFoundError:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
    return username, password
    

def login(driver: webdriver.Chrome | webdriver.Firefox, username, password):
    # Go to the login page
    driver.get("https://sites.carleton.edu/manage/whmcs-admin/login.php")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").submit()

def getClients(driver: webdriver.Chrome | webdriver.Firefox):
    driver.get("https://sites.carleton.edu/manage/whmcs-admin/clients.php")
    time.sleep(5)
    

if __name__ == "__main__":
    driver = getDriver()
    username, password = getCredentials()
    login(driver, username, password)
    getClients(driver)
    # Open the users tab and scrape the user data:
    # TODO: Implement the scraping of the user data
    