import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Pandas Dataframe
ASSET_SHEET = "../asset_information/Hardware_assets.xlsx"
df = pd.read_excel(ASSET_SHEET)

initial_row = df.iloc[0]
print(initial_row['Serial Number'], initial_row['Asset Tag'])

# Grab data from excel sheet
manufacturer = initial_row['Manufacturer']
serial_number = initial_row['Serial Number']
model_number = initial_row['Model']

# Chrome Web Driver
driver = webdriver.Chrome()

# Access Warranty Site
driver.get('http://www.lookupwarranty.com/')

# Grab the elements from the site
mfg = Select(driver.find_element(By.ID, 'mfg'))
serial = driver.find_element(By.ID, 'serial')
model = driver.find_element(By.ID, 'model')
submit = driver.find_element(By.ID, 'submitButton')

# Interact with Site
mfg.select_by_value(manufacturer.lower())
serial.send_keys(serial_number)
model.send_keys(model_number)

# Click Submit?
submit.click()

WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="output"]/table'))
)

warranty_start = driver.find_element(By.XPATH, '//*[@id="output"]/table/tbody/tr[3]/td[2]')
warranty_end = driver.find_element(By.XPATH, '//*[@id="output"]/table/tbody/tr[4]/td[2]')

print(type(warranty_start.text))

'''df.loc[df['Serial Number'] == serial_number, 'Warranty Start'] = warranty_start.text
df.loc[df['Serial Number'] == serial_number, 'Warranty End'] = warranty_end.text'''

time.sleep(100)