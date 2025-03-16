from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


# service = Service(executable_path="chrome-linux64/chrome")
driver = webdriver.Chrome()
#driver.set_page_load_timeout(300)
driver.get('https://www.daraz.pk/catalog/?spm=a2a0e.tm80335142.search.d_go&q=sunglasses')
driver.maximize_window()

image_links = []
for i in range(1,40):
    j = str(i)
    
    image_link = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[{j}]/div/div/div[1]/div/a/div/img').get_attribute('src')
    image_links.append(image_link)


print(image_links)

# WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="searchbox_input"]')))

time.sleep(60)
driver.quit()
