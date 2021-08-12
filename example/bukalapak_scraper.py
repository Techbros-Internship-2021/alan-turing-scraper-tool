import time
import pandas as pd
from tqdm import tqdm
from bs4 import BeautifulSoup
from selenium import webdriver

def get_link(data):
    product_page_link,store_page_link = [],[]
    for element in data:
        product_page = element.find("p", class_ = "bl-text bl-text--body-small bl-text--ellipsis__2").a.get('href')
        store_page = element.find("span", class_ = "bl-product-card__store bl-text bl-text--body-small bl-text--subdued bl-text--ellipsis__1").a.get('href')
        product_page_link.append(product_page),store_page_link.append(store_page)
    return product_page_link,store_page_link

def scraping_product(driver,product_page_link):
    all_product_data = []
    for link in tqdm(product_page_link):
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        product_name = soup.find_all('h1',{'class':'c-main-product__title u-txt--large'})[0].text[:-1]

        try:
            product_price = int(soup.find("div", class_ = "c-product-price -original -main").span.text[2:].replace('.',''))
        except:
            product_price = int(soup.find("div", class_ = "c-product-price -discounted -main").span.text[2:].replace('.','')) 

        try:
            product_rate = float(soup.find("div", class_ = "c-reviews__summary-pie").findAll(lambda tag: tag.name=='span')[0].text)
        except:
            product_rate = 0.0

        try:
            product_num_review = int(soup.find("div", class_ = "c-main-product__rating u-mrgn-right--2").text[1:-7])
        except:
            product_num_review = 0

        try:
            product_num_sold = int(soup.find("div", class_ = "c-main-product__reviews").findAll(lambda tag: tag.name=='span')[-1].text[:-8])
        except:
            product_num_sold = 0

        product_category = (soup.find("table", class_ = "c-information__table").findAll(lambda tag: tag.name=='td'))[1].text

        product_picture = soup.find("div", class_ = "c-bl-media").picture.img.get('src')

        product_specs = soup.find("table", class_ = "c-information__table").findAll(lambda tag: tag.name=='tr')
        product_specs = [value.text for idx,value in enumerate(product_specs) if idx >= 1]

        all_product_data.append([product_name,product_price,product_rate,product_num_review,product_num_sold,product_category,product_picture,product_specs,link])
        driver.implicitly_wait(1.5)
    return all_product_data
    
def scraping_store(driver,store_page_link):
    all_store_data = []
    for link in tqdm(store_page_link):
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, "html.parser")

        store_name = soup.find("h1", class_ = "u-txt--fair u-txt--bold merchant-page__store-name ut-store-name").text[9:-7]

        store_location = soup.find("div", class_ = "u-display-block u-mrgn-bottom--2 u-fg--ash-dark u-txt--small").a.text[11:-9]

        store_rating = (int(soup.find("table", class_ = "c-table c-table--equal c-table--tight").findAll(lambda tag: tag.name=='td')[1].text[:-6])*5)/100

        store_response_duration = soup.find("table", class_ = "c-table c-table--equal c-table--tight").findAll(lambda tag: tag.name=='td')[9].text

        try:
            store_follower = int(soup.find("table", class_ = "c-table c-table--equal c-table--tight").findAll(lambda tag: tag.name=='td')[5].text[12:-9])
        except:
            store_follower = int(soup.find("table", class_ = "c-table c-table--equal c-table--tight").findAll(lambda tag: tag.name=='td')[5].text[12:-9].replace(',',''))
                
        all_store_data.append([store_name,store_location,store_rating,store_response_duration,store_follower,link])
        driver.implicitly_wait(1.5)
    return all_store_data

def get_all_data(product_page_data,store_page_data):
    all_data = []
    for product,store in tqdm(zip(product_page_data,store_page_data)):
        data = {
            'Product name':product[0],'Product price':product[1],'Product rating':product[2],
            'Product review/s':product[3], 'Product sold':product[4],'Product category':product[5],
            'Product picture':product[6],'Product specsification':product[7],'Product Link':product[8],
            'Store Name':store[0],'Store Location':store[1],'Store rating':store[2],'Store process duration':store[3],
            'Store follower':store[4],'Store Link':store[5]
        }
        all_data.append(data)
    
    return all_data

def _get_chrome_option():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    options.headless = True
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--window-size=1920,1080")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    return options

def _get_data():
    # download chromedriver.exe and save in same folder with this file.py
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=_get_chrome_option())
    product = "laptop"
    url = "https://www.bukalapak.com/products?search%5Bkeywords%5D={}".format(product)

    driver.get(url)

    for i in range(10):
	    driver.execute_script("window.scrollTo({top:document.body.scrollHeight,behavior: 'smooth'});")
	    time.sleep(0.15)
    driver.execute_script("window.scrollTo({top: 0,behavior: 'smooth'});")
    time.sleep(0.15)

    soup = BeautifulSoup(driver.page_source, "html.parser")
    data = soup.find_all('div',{'class':'bl-product-card te-product-card'})
    product_page_link, store_page_link = get_link(data)

    return scraping_product(driver,product_page_link),scraping_store(driver,store_page_link)

product_page_data, store_page_data = _get_data()
all_data_scraping = get_all_data(product_page_data, store_page_data)
data_result_df = pd.DataFrame(all_data_scraping)
data_result_df.to_csv(r"C:\Users\User\Documents\Techbros Internship\projects\bukalapak_data_scraper.csv", index=False)
print(data_result_df)
