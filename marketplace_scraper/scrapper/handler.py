# Copyright 2021 Techbros GmbH. All Rights Reserved.
# 
# Unauthorized copying of this file, via any medium is strictly prohibited.
# Proprietary and confidential.
#
# Written by:
# - Okta Fajar Suryani <okta.suryani@techbros.io>
# - Daffa Barin <daffabarin@gmail.com>
# - Ridhwan Nashir <ridhwanashir@gmail.com>
# - Jonas <guterres19dedeus@gmail.com>
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
    
def _blibli_handler_searchpage(driver, **query):

    blibli_utilities = blibliUtilities(driver) # initiate blibli utilities class
    defined_query = query
    link_factory = linkFactory(defined_query)
    print('[INFO] creating url from user query ...')
    url_ref = link_factory._blibli_link_factory()
    print('[INFO] url_ref:', url_ref)
    driver.get(f'{url_ref}')
    print('[INFO] In search page ...')
    
    # waiting for element to appear
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="product__item"]')))
    Product_info_list = driver.find_elements_by_class_name('product__item')
    # start scraping data using blibliutilities
    productslink = blibli_utilities.get_linkproduct(driver,Product_info_list)
    print("[INFO] recorded product num: {}".format(len(productslink)))
    productsname = blibli_utilities.get_nameproduct(driver,Product_info_list)
    productsrating = blibli_utilities.get_ratingproduct(driver,Product_info_list)
    productssold = blibli_utilities.get_soldproduct(driver,Product_info_list)
    productsprice = blibli_utilities.get_priceproduct(driver,Product_info_list)
    productslocation = blibli_utilities.get_locationproduct(driver,Product_info_list)

    result = pd.DataFrame(zip(productsname,productsrating,productssold,productsprice,productslocation,productslink),
            columns= ["Name", "Rating", "Sold", "Price", "Location", "Link"])    
    return result

def _blibli_handler_detailed(driver, **query):
    DataProduct = []
    blibli_utilities = blibliUtilities(driver) # initiate blibli utilities class
    defined_query = query
    link_factory = linkFactory(defined_query)

    print('[INFO] creating url from user query ...')
    url_ref = link_factory._blibli_link_factory()
    print('[INFO] url_ref:', url_ref)
    driver.get(f'{url_ref}')
    print('[INFO] In search page ...')
    
    # waiting for element to appear
    WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@class="product__item"]')))
    Product_info_list = driver.find_elements_by_class_name('product__item')
    # saving each product
    productslink = blibli_utilities.get_linkproduct(driver,Product_info_list)
    print("[INFO] recorded product num: {}".format(len(productslink)))

    # start scraping
    for link in tqdm(productslink):
        driver.get(link)
    #     initiate element with null
        name = rating = review = sold = price = category = spec = picture = sname = sresponse = slocation = followers = srating = None
        scrolling(driver)
        # scrape from products
        try:
            name = driver.find_element_by_xpath('//div[@id="product-info"]/div[2]/div[1]').text
        except NoSuchElementException:
            pass
        try:
            rating = driver.find_element_by_xpath('//div[@class="review-summary__average"]/div[1]').text
        except NoSuchElementException: 
            pass
        try:
            review = driver.find_element_by_xpath('//*[@id="product-review"]/div[2]/div[1]/div[1]/div[1]/div[1]/span').text
        except NoSuchElementException:  
            pass
        try:
            sold = driver.find_element_by_xpath('//*[@id="product-info"]/div[2]/div[2]/span[2]').text
        except NoSuchElementException:  #spelling error making this code not work as expected
            pass
        try:
            price = driver.find_element_by_xpath('//*[@class="final-price"]/span').text
        except NoSuchElementException: 
            pass
        try:
            category = driver.find_element_by_xpath('//*[@class="category"]/a').text
        except NoSuchElementException: 
            pass
        try:
            spec = get_spec(driver)
        except NoSuchElementException:  
            pass
        try:
            picture = get_picture(driver)
        except NoSuchElementException: 
            pass
        try:
            sname = driver.find_element_by_xpath('//div[@class="seller__name"]/a').text
        except NoSuchElementException:  
            pass
        try:
            sresponse = driver.find_element_by_xpath('//div[@class="seller-rating__active-response"]/div[1]/span').text
        except NoSuchElementException:  
            pass
        try:
            slocation = driver.find_element_by_xpath('//div[@class="seller-info__location"]/div[2]/span').text
        except NoSuchElementException:  
            pass
        # scrape from shop (using clicks)
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
        driver.find_element_by_xpath('//button[@class="ticker__close b-order-right"]').click() # close pop up
        driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME) # twice for load more element
        driver.find_element_by_xpath('//div[@class="seller__name"]/a').click() 
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '//p[@class="followers-count"]')))
        try:
            followers = driver.find_element_by_xpath('//p[@class="followers-count"]').text
        except NoSuchElementException:  
            pass
        try:
            srating = driver.find_element_by_xpath('//span[@class="rating-merchant-value no-rating"]/div/span').text
        except NoSuchElementException:  
            pass
        
        listofitems = {
            'Product name':name,'Product Rating':rating,'Total Review':review,
            'Total Sold': sold,'Price':price,'Product Category':category,
            'Product Specs':spec,'Product Picture':picture,'Store Name':sname,'Store Response Duration':sresponse, 
            'Store Location':slocation,'Product Link': link,'Followers': followers,'Store Rating': srating
        }
        DataProduct.append(listofitems)
    result = pd.DataFrame(DataProduct)
    return result

def _bukalapak_handler(driver, **query):

    # your scraping process
    url = "https://www.bukalapak.com/products?search%5Bkeywords%5D={}".format(query['product'])
    driver.get(url)
    time.sleep(2)

    #scrolling through the website
    scrolling(driver)

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
