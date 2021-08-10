# Copyright 2021 Techbros GmbH. All Rights Reserved.
# 
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by:
# - Your Name <your email>
# =========================================================================

import time
import math
import re
import pandas as pd

from bs4 import BeautifulSoup
from tqdm import tqdm


SCROLL_RATE = math.sqrt(2)
SCROLL_PAUSE_TIME = 1.25

# EXAMPLE
def _blibli_handler(driver, **query):
    url = "https://siplah.blibli.com/search?keyword={}&itemPerPage=40&page=0".format(query['product'])
    driver.get(url)
    time.sleep(2)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    data = soup.find_all('button',{'class':'pagination-button'})
    maximum_page = 1
    for element in data:
        if element.findChild('span') is not None:
            temp = int(element.findChild('span').text)
            maximum_page = temp if maximum_page < temp else maximum_page

    product_link = list()
    product_name = list()
    product_price = list()
    product_location = list()
    product_merchant = list()
    for page in tqdm(range(maximum_page), desc ="Scrapper Progress"):
        driver.get("https://siplah.blibli.com/search?keyword={query}&itemPerPage=40&page={page}".format(query=query['product'], page=page))
        time.sleep(2)

        data = soup.find_all('a',{'id':'prd-list[0]'})
        for element in data:
            link = 'https://siplah.blibli.com' + element['href']
            product_link.append(link)

            name = str(element.findChild('h3').text).replace('\n', '')[6:-4]
            product_name.append(name)

            price = int(str(element.find_all('p', {'class': 'product-price'})[0].text).replace('\n', '')[9:-4].replace('.', ''))
            product_price.append(price)

            location = str(element.find_all('p', {'class': 'product-icon'})[0].text).replace('\n', '')[6:-4]
            product_location.append(location)
            
            merchant = str(element.find_all('p', {'class': 'product-merchant-name'})[0].text).replace('\n', '')[6:-4]
            product_merchant.append(merchant)

    product_data = {
        'name' : product_name, 
        'price' : product_price,
        'location' : product_location,
        'merchant' : product_merchant, 
        'link' : product_link,
        }
    result = pd.DataFrame.from_dict(product_data)
    print()

    return result


def _bukalapak_handler(driver, **query):

    # your scraping process
    # each marketplace should return same data
    
    product_data = {
        'name' : product_name, 
        'price' : product_price,
        'location' : product_location,
        'merchant' : product_merchant, 
        'link' : product_link,
        }
    result = pd.DataFrame.from_dict(product_data)
    print()

    return result


def _shopee_handler(driver, **query):

    # your scraping process
    # each marketplace should return same data

    product_data = {
        'name' : product_name, 
        'price' : product_price,
        'location' : product_location,
        'merchant' : product_merchant, 
        'link' : product_link,
        }
    result = pd.DataFrame.from_dict(product_data)
    print()

    return result

def _tokopedia_handler(driver, **query):
    
    # your scraping process
    # each marketplace should return same data

    product_data = {
        'name' : product_name, 
        'price' : product_price,
        'location' : product_location,
        'merchant' : product_merchant, 
        'link' : product_link,
        }
    result = pd.DataFrame.from_dict(product_data)

    return result