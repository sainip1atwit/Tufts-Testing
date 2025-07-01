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
driver.get('https://tufts.service-now.com/now/nav/ui/classic/params/target/alm_hardware.do%3Fsys_id%3D-1%26sys_is_list%3Dtrue%26sys_target%3Dalm_hardware%26sysparm_checked_items%3D%26sysparm_fixed_query%3D%26sysparm_group_sort%3D%26sysparm_list_css%3D%26sysparm_query%3Dmodel_category%253d81feb9c137101000deeabfc8bcbe5dc4%26sysparm_referring_url%3Dalm_hardware_list.do%253fsysparm_query%253dmodel_category%25253D81feb9c137101000deeabfc8bcbe5dc4%25255EEQ%26sysparm_target%3D%26sysparm_view%3D')

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
try:
    skip_for_now = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[3]/div/button'))
    )
    skip_for_now.click()
finally:
    # Catch 'Don't Trust Browser' Element
    try:
        dont_trust = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="dont-trust-browser-button"]'))
        )
        dont_trust.click()
    finally:
        # Play Around With Form Entries
        try:
            model_id = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="sys_display.alm_hardware.model"]'))
            )
            # Usual Model for Hospital Refresh
            model_id.send_keys('Dell Dell Pro Micro Plus QBM1250')
            
            # Other Form Entries
            use_type_elem = driver.find_element(By.XPATH, '//*[@id="alm_hardware.u_use_type"]')
            use_type = Select(use_type_elem)
            managed_by = driver.find_element(By.XPATH, '//*[@id="sys_display.alm_hardware.managed_by"]')
            serial_number = driver.find_element(By.XPATH, '//*[@id="alm_hardware.serial_number"]')

            use_type.select_by_visible_text('Clinical/Hospital')
            managed_by.send_keys('sschad01')
            serial_number.send_keys('XXXXXXX') 

        finally:
            # Click Submit
            time.sleep(30)


        time.sleep(30)