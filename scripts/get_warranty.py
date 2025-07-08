import time
import subprocess
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException

# Helper function to submit computer information
def submit_form(driver, man, serial_no, model_no):
    # Access Warranty Site
    driver.get('http://www.lookupwarranty.com/')

    # Grab the elements from the site
    mfg = Select(driver.find_element(By.ID, 'mfg'))
    serial = driver.find_element(By.ID, 'serial')
    model = driver.find_element(By.ID, 'model')
    submit = driver.find_element(By.ID, 'submitButton')

    # Interact with Site
    mfg.select_by_value(man.lower())
    serial.send_keys(serial_no)
    model.send_keys(model_no)
    submit.click()

def format_date(date):
    new_date = datetime.strptime(date, '%B %d, %Y')
    return new_date.strftime('%m-%d-%Y')

def get_warranty():
    # Load Excel Sheet
    hardware_assets = pd.read_excel("../asset_information/Hardware_assets.xlsx", sheet_name="Hardware Assets")
    df = pd.DataFrame(hardware_assets)

    # Chrome Web Driver
    driver = webdriver.Chrome()

    # Iterate through dataframe rows
    for index, row in df.iterrows():

        # Get form values from row
        manufacturer = row['Manufacturer']
        serial_number = row['Serial Number']
        model_number = row['Model']

        # Input the computer information to the warranty site
        submit_form(driver, manufacturer, serial_number, model_number)
        time.sleep(5)

        # Get warranty information
        output = None
        counter = 0
        try:
            # if there is a table element, skip exception
            output = driver.find_element(By.XPATH, '//*[@id="output"]/table')

        except NoSuchElementException:
            # if there is not a table element, resubmit until there is
            # Only runs 5 times
            while(not output and counter < 5):
                try:
                    driver.refresh()
                    submit_form(driver, manufacturer, serial_number, model_number)
                    time.sleep(3)
                    output = driver.find_element(By.XPATH, '//*[@id="output"]/table')
                except NoSuchElementException:
                    output = None
                    counter += 1

        # If warranty information was found, add warranty dates
        try:
            # Make sure the dates are the way TechConnect expects it
            warranty_start = format_date(driver.find_element(By.XPATH, '//*[@id="output"]/table/tbody/tr[3]/td[2]').text)
            warranty_end = format_date(driver.find_element(By.XPATH, '//*[@id="output"]/table/tbody/tr[4]/td[2]').text)
        # If no warranty info was found, add blank strings (SHOW MUST GO ON)
        except NoSuchElementException:
            warranty_start = ""
            warranty_end = ""

        # Add Warranty Information to Dataframe
        df.loc[df['Serial Number'] == serial_number, ['Warranty Start', 'Warranty End']] = [warranty_start, warranty_end]

        # Add the config name
        df.loc[df['Serial Number'] == serial_number, ['Config Name']] = 'GVHOSL' + str(row['Asset Tag'])

        driver.refresh()
        time.sleep(3)

    # Rewrite Excel Sheet with dataframce
    with pd.ExcelWriter("../asset_information/Hardware_assets.xlsx", engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, sheet_name="Hardware Assets", index=False)

    subprocess.run(['start', '../asset_information/Hardware_assets.xlsx'], shell=True, check=True)