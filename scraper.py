import sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
# import getpass # for password input

def getDriver():
    # Set up the driver
    driver = webdriver.Chrome()
    driver.implicitly_wait(10)
    return driver

def login(driver: webdriver.Chrome | webdriver.Firefox, username, password):
    # Go to the login page
    driver.get("https://sites.carleton.edu/manage/whmcs-admin/login.php")
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").submit()
    



if __name__ == "__main__":
    # Get the username and password
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    # Get driver:
    driver = getDriver()
    login(driver, username, password)
    # Open the users tab and scrape the user data:
    # TODO: Implement the scraping of the user data
    