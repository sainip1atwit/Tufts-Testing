import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Pandas Dataframe
ASSET_SHEET = "../asset_information/Hardware_assets.xlsx"
df = pd.read_excel(ASSET_SHEET)

initial_row = df.iloc[0]
print(initial_row['Serial Number'], initial_row['Asset Tag'])

# Chrome Web Driver
driver = webdriver.Chrome()

# Access Dell Warranty Site
driver.get('https://www.dell.com/support/contractservices/en-us')

try:
    # Find the warranty lookup input
    warranty_lookup = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="homemfe-dropdown-input"]'))
    )
    warranty_lookup.send_keys(initial_row['Serial Number'])
finally:
    # Click search
    search_button = driver.find_element(By.XPATH, '//*[@id="btnSubmit"]')
    search_button.click()

    # Wait for information to load
    try:
        driver.implicitly_wait(10)
        review_services = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="mfe-productdetails"]/div[2]/div[2]/div[2]/div/div[1]/div[4]/div[1]/a/button'))
        )
        review_services.click()
    finally:
        time.sleep(30)