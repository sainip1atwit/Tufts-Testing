import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver import ActionChains

def create_records():
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

    # Get Excel Data
    hardware_assets = pd.read_excel("../asset_information/Hardware_assets.xlsx", sheet_name="Hardware Assets")
    df = pd.DataFrame(hardware_assets)

    # Iterrate through excel and create a record for each row
    for index, row in df.iterrows():

        model_id = str(row['Model ID'])
        serial_number = (row['Serial Number'])
        asset_tag = str(row['Asset Tag'])
        managed_by = str(row['Managed By'])
        warranty_start = str(row['Warranty Start'])
        warranty_end = str(row['Warranty End'])
        config_name = str(row['Config Name'])

        # Keeping the comments, they are hilarious
        #[!]WTF Shadow-root BS might be worse than iframe nonsense.
        # Shadow host is top level shadow root object (find by CSS only)
        shadow_host = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body > macroponent-f51912f4c700201072b211d4d8c26010'))
        )
        time.sleep(3)
        shadow_root = shadow_host.shadow_root

        #[!]switch to the proper iframe (iframes suck); in this case the whole inner page is an iframe, remember this!
        # Worth noting that only new way of finding elements (find_element(By.Something, 'something')) works with shadowDOM methods
        iframe = WebDriverWait(shadow_root, 5).until(
            EC.presence_of_element_located((By.ID, 'gsft_main'))
        )
        driver.switch_to.frame(iframe)

        # Tabs
        contracts = driver.find_element(By.XPATH, '//*[@id="tabs2_section"]/span[4]/span[1]')

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
        start = driver.find_element(By.XPATH, '//*[@id="alm_hardware.u_warranty_start"]')
        end = driver.find_element(By.XPATH, '//*[@id="alm_hardware.warranty_expiration"]')

        # Add Entries General Page
        model.send_keys(model_id)
        asset.send_keys(asset_tag)
        use_type.select_by_value('Clinical/Hospital')
        managed.send_keys(managed_by)
        serial.send_keys(serial_number)

        # Change over to Contracts Page
        contracts.click()
        start.send_keys(warranty_start)
        end.send_keys(warranty_end)

        # Save Record
        action = ActionChains(driver)
        action.context_click(nav_bar).perform()
        save = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="context_1"]/div[2]'))
        )
        save.click()

        time.sleep(3)
        # Open Configuration Item Page
        config_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="viewr.alm_hardware.ci"]'))
        )
        config_button.click()
        time.sleep(3)
        open_record = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Open Record")]'))
        )
        open_record.click()
        time.sleep(3)

        # Change Configuration Item Name
        config = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="cmdb_ci_computer.name"]'))
        )
        config.clear()
        config.send_keys(config_name)

        # Update the Record
        update_button = driver.find_element(By.XPATH, '//*[@id="sysverb_update"]')
        update_button.click()
        print(f'Record Created for {config_name}')
        
        # Make sure general page is the last tab clicked
        # TechConnect remembers the tab you were last on 
        # When refreshed
        time.sleep(3)
        general = driver.find_element(By.XPATH, '//*[@id="tabs2_section"]/span[1]/span[1]')
        general.click()

        # Multiple refreshes to avoid element not interactable errors
        driver.get(str(HARDWAREURL))
        time.sleep(3)
        driver.get(str(HARDWAREURL))
        time.sleep(3)
        driver.get(str(HARDWAREURL))
        time.sleep(3)

    print('Records Created')
    time.sleep(5)