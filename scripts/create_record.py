import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from selenium.webdriver.support.select import Select

# Load the .env file
load_dotenv()

# Start the chrome web driver
driver = webdriver.Chrome()

# Access New Computer Asset Form
HARDWAREURL = os.getenv('HARDWAREURL')
driver.get(HARDWAREURL)

# Set up for the auth redirect
username = driver.find_element(By.ID, 'username')
password = driver.find_element(By.ID, 'password') 
submit = driver.find_element(By.XPATH, '//*[@id="login"]/button')

# Send username and password entries
username.send_keys(os.getenv('TUFTSUSER'))
password.send_keys(os.getenv('TUFTSPASS'))

# Submit login
submit.click()

# Catch 'Skip For Now' Element in new page
skip_for_now = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[3]/div/button'))
)
skip_for_now.click()

# Catch 'Don't Trust Browser' Element
dont_trust = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="dont-trust-browser-button"]'))
)
dont_trust.click()

# Switch to frame
WebDriverWait(driver, 30).until(lambda d: d.current_url == HARDWAREURL)
driver.switch_to.default_content()
driver.implicitly_wait(10)
driver.switch_to.frame('gsft_main')

time.sleep(100)