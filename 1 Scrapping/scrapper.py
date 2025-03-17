from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.get('https://www.daraz.pk/catalog/?spm=a2a0e.tm80335142.search.d_go&q=sunglasses')
driver.maximize_window()

image_links = []
for i in range(1,40):
    j = str(i)
    
    image_link = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div['+ j +']/div/div/div[1]/div/a/div/img').get_attribute('src')
    image_links.append(str(image_link))
    # print(image_link)

#image_link = driver.find_element(By.XPATH, f'//*[@id="root"]/div/div[2]/div[1]/div/div[1]/div[2]/div[1]/div/div/div[1]/div/a/div/img').get_attribute('src')
print(image_links)

time.sleep(60)
driver.quit()
