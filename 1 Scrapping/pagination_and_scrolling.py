"""
==================================================
 Script Name : pagination_and_scrolling.py
 Description : Scraping comments of multiple pages using pagination and comment - no multithreading.
 Author      : Sakib Ahamed
 Copyright   : © 2025 Sakib. 
 License     : This script is free to use, modify, and distribute 
               for any purpose with attribution. No warranty provided.
==================================================
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import time


driver = webdriver.Chrome()
driver.refresh()
driver.get('https://www.daraz.pk/catalog/?page=1&q=perfume&spm=a2a0e.tm80335142.search.d_go')
driver.maximize_window()

extracted_urls_of_items = [] # all the product urls of a certain type will be stored here
product_details = [] # product name and their comments will be stored in this list in dict format

text_for_total_items = driver.find_element(By.XPATH, '/html/body/div[4]/div/div[2]/div[1]/div/div[1]/div[1]/div/div[1]/div/div/span[1]').text # total items of a type
# print("total number of items: ",text_for_total_items)

match = re.search(r'\b\d+\b', text_for_total_items)
total_items = 0
if match:
    total_items = match.group()
total_number_pages = round(int(total_items)/40)

# function to extract all the urls of a certain search type
def extract_urls(number_of_pages_to_scrape):
    for i in range(1,number_of_pages_to_scrape+1):
        i = str(i)
        driver.get(f'https://www.daraz.pk/catalog/?page={i}&q=perfume&spm=a2a0e.tm80335142.search.d_go')
        time.sleep(int(i)+2)
        element = driver.find_elements(By.XPATH, '/html/body/div[4]/div/div[2]/div[1]/div/div[1]/div[2]/*/div/div/div[2]/div[2]/a')
        extracted_urls_of_items.extend([item.get_attribute('href') for item in element])


# Function to scrape comments of each product -- uses scrolling to load comments.
def get_comments():
    for url in extracted_urls_of_items:
        driver.get(url)
        time.sleep(3)

        # Scroll to the comments section
        height = driver.execute_script('return document.body.scrollHeight')
        for i in range(0, height-500, 50):
            driver.execute_script(f'window.scrollTo(0,{i});')
            time.sleep(0.5)

        comments = [] # All the comments of a product will be temporarily stored here
        product_name = driver.find_element(By.CLASS_NAME, 'pdp-mod-product-badge-title').text
        try:
            total_comment_pages = int(driver.find_element(By.XPATH, '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/div/button[5]').text)
        except Exception as e:
            print("[-] Could not fetch total comments in this page!!", e)

        try:
            for page in range(1,total_number_pages):
                time.sleep(1)
                
                page_comments = driver.find_elements(By.CLASS_NAME, 'content')
                comments.extend([comment.text for comment in page_comments])

                # next_button = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]')
                if page < total_comment_pages:
                    try:
                        next_button = driver.find_element(By.XPATH, 
                            '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]')
                        driver.execute_script("arguments[0].click();", next_button)  
                        time.sleep(2)
                    except Exception as e:
                        print("[-] Next button not found:", e)
                        break
        except:
            print("Could not fetch comments.")

        product_dict = {
                "Product Name": product_name,
                "Product url": url,
                "Comments": comments
            }
        product_details.append(product_dict)


extract_urls(total_number_pages)
get_comments()
print(product_details)


time.sleep(10)
driver.quit()