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
driver.get(str(HARDWAREURL))

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

time.sleep(3)
#[!]WTF Shadow-root BS might be worse than iframe nonsense.
# Shadow host is top level shadow root object (find by CSS only)
shadow_host = driver.find_element(By.CSS_SELECTOR, 'body > macroponent-f51912f4c700201072b211d4d8c26010')
time.sleep(3)
shadow_root = shadow_host.shadow_root

time.sleep(3)
#[!]switch to the proper iframe (iframes suck); in this case the whole inner page is an iframe, remember this!
# Worth noting that only new way of finding elements (find_element(By.Something, 'something')) works with shadowDOM methods
iframe = shadow_root.find_element(By.ID, 'gsft_main')
driver.switch_to.frame(iframe)

time.sleep(3)

# Get Record Information Page 1
asset = driver.find_element(By.XPATH, '//*[@id="alm_hardware.asset_tag"]')
managed = driver.find_element(By.XPATH, '//*[@id="sys_display.alm_hardware.managed_by"]')
serial = driver.find_element(By.XPATH, '//*[@id="alm_hardware.serial_number"]')
model = driver.find_element(By.XPATH, '//*[@id="sys_display.alm_hardware.model"]')

# Contracts Page
contracts = driver.find_element(By.XPATH, '//*[@id="tabs2_section"]/span[4]/span[1]')
warranty_start = driver.find_element(By.XPATH, '//*[@id="alm_hardware.u_warranty_start"]')
warranty_end = driver.find_element(By.XPATH, '//*[@id="alm_hardware.warranty_expiration"]')

time.sleep(100)