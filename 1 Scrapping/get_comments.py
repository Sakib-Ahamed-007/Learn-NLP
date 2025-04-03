from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

import re
import time


driver = webdriver.Chrome()
driver.get('https://www.daraz.pk/products/2-100-i502488465-s2401145772.html?c=&channelLpJumpArgs=&clickTrackInfo=query%253Aperfume%253Bnid%253A502488465%253Bsrc%253ALazadaMainSrp%253Brn%253Aed79a7662612548af3c5927d0e0389e8%253Bregion%253Apk%253Bsku%253A502488465_PK%253Bprice%253A458%253Bclient%253Adesktop%253Bsupplier_id%253A6005227984485%253Bbiz_source%253Ahttps%253A%252F%252Fwww.daraz.pk%252F%253Bslot%253A0%253Butlog_bucket_id%253A470687%253Basc_category_id%253A10002064%253Bitem_id%253A502488465%253Bsku_id%253A2401145772%253Bshop_id%253A1760775%253BtemplateInfo%253A1103_L%2523-1_A3_C%2523&freeshipping=0&fs_ab=1&fuse_fs=&lang=en&location=Punjab&price=458&priceCompare=skuId%3A2401145772%3Bsource%3Alazada-search-voucher%3Bsn%3Aed79a7662612548af3c5927d0e0389e8%3BoriginPrice%3A45800%3BdisplayPrice%3A45800%3BsinglePromotionId%3A50000023246003%3BsingleToolCode%3AflashSale%3BvoucherPricePlugin%3A0%3Btimestamp%3A1743553799452&ratingscore=4.343478260869565&request_id=ed79a7662612548af3c5927d0e0389e8&review=230&sale=1985&search=1&source=search&spm=a2a0e.searchlist.list.0&stock=1')
driver.maximize_window()
driver.refresh()
time.sleep(3)
height = driver.execute_script('return document.body.scrollHeight')

product_details = []
total_comment_pages = int(driver.find_element(By.XPATH, '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/div/button[5]').text)

for i in range(0,height-500,50):
    driver.execute_script(f'window.scrollTo(0,{i});')
    time.sleep(0.5)

product_name = driver.find_element(By.CLASS_NAME, 'pdp-mod-product-badge-title').text

for page in range(1,total_comment_pages+1):
    time.sleep(2)
    comments = []
    page_comments = driver.find_elements(By.CLASS_NAME, 'content')
    comments.extend([comment.text for comment in page_comments])

    product_dict = {
        "Product Name": product_name,
        # "Product url": url,
        "Comments": comments
    }
    product_details.append(product_dict)

    # next_button = driver.find_element(By.XPATH, '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]')
    if page < total_comment_pages:
        try:
            next_button = driver.find_element(By.XPATH, 
                '/html/body/div[5]/div/div[10]/div[1]/div[2]/div/div/div/div[3]/div[2]/div/button[2]')
            driver.execute_script("arguments[0].click();", next_button)  
            time.sleep(2)
        except Exception as e:
            print("Next button not found:", e)
            break

print(product_details)

time.sleep(10)
driver.quit()