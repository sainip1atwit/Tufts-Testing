import os
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Start the chrome web driver
driver = webdriver.Chrome()

# Access Tech Connect
driver.get('http://tufts.service-now.com')

# Set up for the auth redirect
username = driver.find_element(By.ID, 'login_id')
password = driver.find_element(By.ID, 'password')

username.send_keys(os.getenv('USERNAME'))
password.send_keys(os.getenv('PASSWORD'))