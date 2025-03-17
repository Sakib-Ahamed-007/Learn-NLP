from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import time

driver = webdriver.Chrome()
driver.get('https://www.google.com/maps/search/top+10+real+estate+company+in+bangladesh/@23.7960418,90.3459925,13z/data=!4m3!2m2!5m1!4e3?hl=en&entry=ttu&g_ep=EgoyMDI1MDMxMi4wIKXMDSoASAFQAw%3D%3D')
driver.maximize_window()

top_companies = []
wait = WebDriverWait(driver, 10)

# Loop through each company entry and click each entry to open the data frame of that entry
for i in range(3, 22, 2):
    j = str(i)

    company_element = wait.until(EC.presence_of_element_located((By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{j}]/div/a')))
    company_element.send_keys(Keys.ENTER) # Click enter button on each company to open it's data frame

    time.sleep(5)
    
    company_name = company_element.get_attribute('aria-label')
    try:
        company_website = driver.find_element(By.XPATH, '//a[contains(@aria-label, "Website")]').get_attribute('href')
    except NoSuchElementException:
        company_website = "Not Found"
    
    try:
        company_phone_number = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Phone")]/div/div[2]/div[1]').text
    except NoSuchElementException:
        company_phone_number = "Not Found"
    
    try:
        company_location = driver.find_element(By.XPATH, '//button[contains(@aria-label, "Address")]/div/div[2]/div[1]').text
    except NoSuchElementException:
        company_location = "Not Found"

    # Dictionary containing all the data of the company
    company_dict = {
        "Company Name:": company_name,
        "Company Location": company_location,
        "Company Phone NUmber": company_phone_number,
        "Company Website": company_website
    }
    top_companies.append(company_dict)

for company in top_companies:
    print(company)

time.sleep(10)
driver.quit()

