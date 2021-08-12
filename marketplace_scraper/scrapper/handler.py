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
    url = "https://www.bukalapak.com/products?search%5Bkeywords%5D={}".format(query['product'])
    driver.get(url)
    time.sleep(2)

    for i in range(10):
        driver.execute_script("window.scrollTo({top:document.body.scrollHeight,behavior: 'smooth'});")
        time.sleep(0.15)
    driver.execute_script("window.scrollTo({top: 0,behavior: 'smooth'});")
    time.sleep(0.15)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    data = soup.find_all('div',{'class':'bl-product-card te-product-card'})
    product_page_link, store_page_link = [],[]
    product_names,product_prices,product_rates,product_num_reviews = list(),list(),list(),list()
    product_nums_sold,product_categories,product_pictures,product_specs,product_links = list(),list(),list(),list(),list()
    store_names,store_locations,store_rates,store_responses_duration,store_followers,store_links = list(),list(),list(),list(),list(),list()

    for element in data:
        product_page = element.find("p", class_ = "bl-text bl-text--body-small bl-text--ellipsis__2").a.get('href')
        store_page = element.find("span", class_ = "bl-product-card__store bl-text bl-text--body-small bl-text--subdued bl-text--ellipsis__1").a.get('href')
        product_page_link.append(product_page),store_page_link.append(store_page)
        
    for product_link, store_link in tqdm(zip(product_page_link,store_page_link)):
        driver.get(product_link)
        product_links.append(product_link)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        product_name = soup.find_all('h1',{'class':'c-main-product__title u-txt--large'})[0].text[:-1]
        product_names.append(product_name)

        try:
            product_price = int(soup.find("div", class_ = "c-product-price -original -main").span.text[2:].replace('.',''))
        except:
            product_price = int(soup.find("div", class_ = "c-product-price -discounted -main").span.text[2:].replace('.','')) 
        product_prices.append(product_price)

        try:
            product_rate = float(soup.find("div", class_ = "c-reviews__summary-pie").findAll(lambda tag: tag.name=='span')[0].text)
        except:
            product_rate = 0.0
        product_rates.append(product_rate)

        try:
            product_num_review = int(soup.find("div", class_ = "c-main-product__rating u-mrgn-right--2").text[1:-7])
        except:
            product_num_review = 0
        product_num_reviews.append(product_num_review)

        try:
            product_num_sold = int(soup.find("div", class_ = "c-main-product__reviews").findAll(lambda tag: tag.name=='span')[-1].text[:-8])
        except:
            product_num_sold = 0
        product_nums_sold.append(product_num_sold)

        product_category = (soup.find("table", class_ = "c-information__table").findAll(lambda tag: tag.name=='td'))[1].text
        product_categories.append(product_category)

        product_picture = soup.find("div", class_ = "c-bl-media").picture.img.get('src')
        product_pictures.append(product_picture)

        product_spec = soup.find("table", class_ = "c-information__table").findAll(lambda tag: tag.name=='tr')
        product_spec = [value.text for idx,value in enumerate(product_spec) if idx >= 1]
        product_specs.append(product_spec)

        driver.implicitly_wait(1.5)
        
        driver.get(store_link)
        store_links.append(store_link)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        store_name = soup.find("h1", class_ = "u-txt--fair u-txt--bold merchant-page__store-name ut-store-name").text[9:-7]
        store_names.append(store_name)

        store_location = soup.find("div", class_ = "u-display-block u-mrgn-bottom--2 u-fg--ash-dark u-txt--small").a.text[11:-9]
        store_locations.append(store_location)

        store_rate = float((int(soup.find("table", class_ = "c-table c-table--equal c-table--tight").findAll(lambda tag: tag.name=='td')[1].text[:-6])*5)/100)
        store_rates.append(store_rate)
        
        store_response_duration = soup.find("table", class_ = "c-table c-table--equal c-table--tight").findAll(lambda tag: tag.name=='td')[9].text
        store_responses_duration.append(store_response_duration)

        try:
            store_follower = int(soup.find("table", class_ = "c-table c-table--equal c-table--tight").findAll(lambda tag: tag.name=='td')[5].text[12:-9])
        except:
            store_follower = int(soup.find("table", class_ = "c-table c-table--equal c-table--tight").findAll(lambda tag: tag.name=='td')[5].text[12:-9].replace(',',''))
        store_followers.append(store_follower)

        driver.implicitly_wait(1.5)
    # each marketplace should return same data
    All_data = {
        'Product name':product_names,'Product price':product_prices,'Product rating':product_rates,
        'Product review/s':product_num_reviews, 'Product sold':product_nums_sold,'Product category':product_categories,
        'Product picture':product_pictures,'Product specsification':product_specs,'Product Link':product_links,
        'Store Name':store_names,'Store Location':store_locations,'Store rating':store_rates,'Store process duration':store_responses_duration,
        'Store follower':store_followers,'Store Link':store_links
    }
    result = pd.DataFrame.from_dict(All_data)
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
