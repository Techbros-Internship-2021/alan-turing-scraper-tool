# Copyright 2021 Techbros GmbH. All Rights Reserved.
# 
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by:
# - Okta Fajar Suryani <okta.suryani@techbros.io>
# - Daffa Barin <daffabarin@gmail.com>
# - Ridhwan Nashir <ridhwanashir@gmail.com>
# - Jonas de Deus Guterres <guterres19dedeus@gmail.com>
# =========================================================================

import time
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm
from marketplace_scraper.scrapper.factory import shopeeUtilities, linkFactory

# EXAMPLE
def scrolling(driver):
    for i in reversed(range(10)):
        driver.execute_script("window.scrollTo({top:document.body.scrollHeight,behavior: 'smooth'});")
        time.sleep(1)
    time.sleep(2)
    
def _blibli_handler(driver, **query):
    pass

def _bukalapak_handler(driver, **query):

    defined_query = query
    link_factory = linkFactory(defined_query)
    print('[INFO] creating url from user query ...')
    url_ref = link_factory._bukalapak_link_factory()
    print('[INFO] url_ref:', url_ref)
    driver.get(f'{url_ref}')
    scrolling(driver)

    print('[INFO] In search page ...')
    time.sleep(3)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    data = soup.find_all('div',{'class':'bl-product-card te-product-card'})
    data = data[:defined_query['Num Search']] if len(data) >= defined_query['Num Search'] else data
    product_names,product_prices,product_rates = list(),list(),list()
    product_nums_sold,product_pictures,product_links = list(),list(),list()
    store_locations = list()
        
    for element in data:

        product_picture =  element.find("div",class_ = "bl-thumbnail--slider").div.a.img.get('src')
        product_pictures.append(product_picture)

        product_name = element.find("p",class_ = "bl-text bl-text--body-small bl-text--ellipsis__2").a.text[13:-11]
        product_names.append(product_name)
        
        product_price = int(element.find("p",class_ = "bl-text bl-text--subheading-2 bl-text--semi-bold bl-text--ellipsis__1").text[13:-9].replace('.',''))
        product_prices.append(product_price)

        try:
            product_rate = float(element.find("div",class_ = "bl-product-card__description-rating-and-sold").div.p.a.text[15:-13])
        except:
            product_rate = 0.0
        product_rates.append(product_rate)

        try:
            product_num_sold = int(element.find("div",class_ = "bl-product-card__description-rating-and-sold").findAll(lambda tag: tag.name=='p')[-1].text[19:-9])
        except:
            product_num_sold = 0
        product_nums_sold.append(product_num_sold)
        
        product_link = element.find("p", class_ = "bl-text bl-text--body-small bl-text--ellipsis__2").a.get('href')
        product_links.append(product_link)

        store_location = element.find("span",class_ = "mr-4 bl-product-card__location bl-text bl-text--body-small bl-text--subdued bl-text--ellipsis__1").text[11:-9] 
        store_locations.append(store_location)

    # each marketplace should return same data
    All_data = {
        'Product name':product_names,'Product price':product_prices,'Product rating':product_rates,
        'Product sold':product_nums_sold,'Product picture':product_pictures,'Product Link':product_links,
        'Store Location':store_locations
    }
    result = pd.DataFrame.from_dict(All_data)
    print()

    return result


def _shopee_handler(driver,  **query):

    defined_query = query
    link_factory = linkFactory(defined_query)
    print('[INFO] creating url from user query ...')
    url_ref = link_factory._shopee_link_factory()
    print('[INFO] url_ref:', url_ref)
    driver.get(f'{url_ref}')
    scrolling(driver)
    print('[INFO] In search page ...')
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")

    link_each_product_list = list()
    product_name_list = list()
    product_rating_list = list()
    product_num_review_list = list()
    product_num_sold_list = list()
    product_price_list = list()
    product_spec_list = list()
    product_category_list = list()
    product_images_link_list = list()
    store_name_list = list()
    store_response_duration_list = list()
    store_location_list = list()
    store_follower_list = list()
    store_rating_list = list()

    item_element_div = soup.find_all('div',{'class':'col-xs-2-4 shopee-search-item-result__item'})
    print('[INFO] len(item_element_div):', len(item_element_div))
    for item_element in item_element_div:
        link_product_div = item_element.find_all('a', {'data-sqe': 'link'})
        print('[INFO] len(link product div):', len(link_product_div))
        if len(link_product_div) > 0:
            for each_link in link_product_div:
                link_each_product = 'https://shopee.co.id'+each_link.get('href')
            print('[INFO] product url:', link_each_product)
            link_each_product_list.append(link_each_product)
            loc_each_product = item_element.find_all('div', {'class': '_2CWevj'})[0].text.strip()
            print('[INFO] store location:', loc_each_product)
            store_location_list.append(loc_each_product)
    
    print('INFO] len(store_location_list):', len(store_location_list))
    print('INFO] len(link_each_product_list):', len(link_each_product_list))
    assert len(store_location_list) == len(link_each_product_list)

    if len(link_each_product_list) >= defined_query['Num Search'] and len(store_location_list)  >= defined_query['Num Search']:
        link_each_product_list = link_each_product_list[:defined_query['Num Search']]
        store_location_list = store_location_list[:defined_query['Num Search']]
    
    for idx, link_item in enumerate(link_each_product_list):
        print(f'[INFO] scraping {idx+1}/{len(link_each_product_list)} data ...')
        driver.get(link_item)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        shopee_utilities = shopeeUtilities(soup)
        product_name = shopee_utilities.get_product_name()
        product_name_list.append(product_name)
        product_rating = shopee_utilities.get_product_rating()
        product_rating_list.append(product_rating)
        product_num_review = shopee_utilities.get_product_num_review()
        product_num_review_list.append(product_num_review)
        product_num_sold = shopee_utilities.get_product_num_sold()
        product_num_sold_list.append(product_num_sold)
        product_price = shopee_utilities.get_product_price()
        product_price_list.append(product_price)
        product_spec = shopee_utilities.get_product_spec()
        product_spec_list.append(product_spec)
        product_category = shopee_utilities.get_product_category()
        product_category_list.append(product_category)
        product_image_link = shopee_utilities.get_product_images_link()
        product_images_link_list.append(product_image_link)
        store_name = shopee_utilities.get_store_name()
        store_name_list.append(store_name)
        store_response_duration = shopee_utilities.get_store_response_duration()
        store_response_duration_list.append(store_response_duration)
        store_follower = shopee_utilities.get_store_follower()
        store_follower_list.append(store_follower)

        driver.find_element_by_xpath('//div[@class="_34c6X6 page-product__shop"]/div[1]/a').click()
        time.sleep(3)
        print('[INFO] In store page ...')
        store_rating = driver.find_element_by_xpath('//div[@class="shop-page__info"]/div/div[2]/div[5]/div[2]/div[2]').text
        store_rating = float(store_rating.split(' ')[0])
        store_rating_list.append(store_rating)

    product_data = {
        'Product name':product_name_list,'Product price':product_price_list,'Product rating':product_rating_list,
        'Product review/s':product_num_review_list, 'Product sold':product_num_sold_list,'Product category':product_category_list,
        'Product picture':product_images_link_list,'Product specsification':product_spec_list,'Product Link':link_each_product_list,
        'Store Name':store_name_list,'Store Location':store_location_list,'Store rating':store_rating_list,
        'Store process duration':store_response_duration_list,'Store follower':store_follower_list
    }
    result = pd.DataFrame.from_dict(product_data)
    return result

def _tokopedia_handler(driver, **query):
    #get query from front-end
    url = "https://www.tokopedia.com/search?st=product&q={}".format(query['product'])
    driver.get(url)
    time.sleep(2)
    
    #scrolling through the website
    scrolling(driver)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    data = soup.find_all('div',{'class':'css-7fmtuv'})
    productsLinks = []
    for element in data:
        productsLinks.append(element.a.get('href'))
    productsLinks = [x for x in productsLinks if not x.startswith("https://ta.tokopedia.com/")]

    result = []
    for link in tqdm(productsLinks[:10]):
        driver.get(link)
        time.sleep(1)
        scrolling(driver)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        # Product
        productName = soup.find("h1", class_ = "css-1wtrxts").text
        productRating = soup.find_all("span", class_ = "main")[1].text
        productNumReview = int(soup.find("span", attrs={"data-testid":"lblPDPDetailProductRatingCounter"}).text[1:3]) if soup.find("span", attrs={"data-testid":"lblPDPDetailProductRatingCounter"}) else 0
        productNumSold = int(soup.find("div", attrs={"data-testid":"lblPDPDetailProductSoldCounter"}).text.replace("Terjual ",'')) if soup.find("div", attrs={"data-testid":"lblPDPDetailProductSoldCounter"}) else 0
        productPrice = int(soup.find("div", class_ = "price").text.replace("Terjual ",'')[2:].replace('.','')) if soup.find("div",class_ = "price") else 0
        productCategory = soup.find("ul", class_ = "css-1ijyj3z e1iszlzh2").find_all("li",class_ ="css-1dmo88g")[2].text[10:] if soup.find("ul", class_ = "css-1ijyj3z e1iszlzh2") else soup.find_all("li", class_ ="css-1dmo88g")[3].text[10:]
        productSpecs = soup.find("span", class_ = "css-17zm3l e1iszlzh1").text
        productPicture = soup.find("div", class_ = "css-19i5z4j").img.get('src')

        # Store
        storeName = soup.find("a", class_ = "css-1n8curp").text
        storeRating = float(soup.find("div", class_ = "css-1rktnzx").text.replace("rata-rata ulasan","")) if soup.find("div", class_ = "css-1rktnzx") else 0
        #go to store page
        storeLink = "https://tokopedia.com{}".format(soup.find("a", class_ = "css-1n8curp").get("href"))
        driver.get(storeLink)
        time.sleep(3)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        time.sleep(1)
        storeResponseDuration = soup.find("p", class_ = "css-larfgg-unf-heading-unf-heading e1qvo2ff8").text[10:]
        storeLocation = soup.find_all("p", class_ = "css-larfgg-unf-heading-unf-heading e1qvo2ff8")[1].text
        storeFollowers = soup.find("h6", class_ = "css-1xrfbuw-unf-heading-unf-heading e1qvo2ff6").text.replace(" Followers","")

        datum = {
                    'Product name':productName,'Product price':productPrice,'Product rating':productRating,
                    'Product review/s':productNumReview, 'Product sold':productNumSold,'Product category':productCategory,
                    'Product picture':productPicture,'Product specification':productSpecs,'Product Link':"linklinklink",
                    'Store Name':storeName,'Store Location':storeLocation,'Store rating':storeRating,'Store Response duration':storeResponseDuration,
                    'Store Followers':storeFollowers,'Store Link':storeLink
                }
        result.append(datum)
    return result
