import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains
from dotenv import load_dotenv

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
'''skip_for_now = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[3]/div/button'))
)
skip_for_now.click()'''

# Catch 'Don't Trust Browser' Element
dont_trust = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="dont-trust-browser-button"]'))
)
dont_trust.click()
time.sleep(5)

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

# Tabs
contracts = driver.find_element(By.XPATH, '//*[@id="tabs2_section"]/span[4]/span[1]')
general = driver.find_element(By.XPATH, '//*[@id="tabs2_section"]/span[1]/span[1]')

# Nav Bar to Save and Remain in Record
nav_bar = driver.find_element(By.XPATH, '//*[@id="section-faeaf24c37f3100044e0bfc8bcbe5d9a.header"]/nav')

# General Page
asset = driver.find_element(By.XPATH, '//*[@id="alm_hardware.asset_tag"]')
managed = driver.find_element(By.XPATH, '//*[@id="sys_display.alm_hardware.managed_by"]')
serial = driver.find_element(By.XPATH, '//*[@id="alm_hardware.serial_number"]')
model = driver.find_element(By.XPATH, '//*[@id="sys_display.alm_hardware.model"]')

# Values for Use Type
# Classroom - Instrument 
# Classroom - Workstation
# Department Shared
# Faculty/Staff
# Loaner
# Public - Kiosk
# Public - Loaner
# Public - Workstation
# Public - Remote Lab
# Research - Instrument
# Research - Workstation
# Clinical/Hospital
use_type = Select(driver.find_element(By.XPATH, '//*[@id="alm_hardware.u_use_type"]'))

# Contracts Page
warranty_start = driver.find_element(By.XPATH, '//*[@id="alm_hardware.u_warranty_start"]')
warranty_end = driver.find_element(By.XPATH, '//*[@id="alm_hardware.warranty_expiration"]')

# Add Entries General Page
model.send_keys('Dell Dell Pro Micro Plus QBM1250')
asset.send_keys('99999')
use_type.select_by_value('Clinical/Hospital')
managed.send_keys('sschad01')
serial.send_keys('XXXXXXXX')

# Change over to Contracts Page
contracts.click()
warranty_start.send_keys('07-07-2025')
warranty_end.send_keys('07-07-2028')

# Right Click Nav Bar
action = ActionChains(driver)
action.context_click(nav_bar).perform()
save = WebDriverWait(driver, 3).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="context_1"]/div[2]'))
)

time.sleep(100)