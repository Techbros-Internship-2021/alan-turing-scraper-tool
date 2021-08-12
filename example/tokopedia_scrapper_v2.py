import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
import time
from bs4 import BeautifulSoup

def scrolling(driver):
    for i in reversed(range(10)):
        driver.execute_script("window.scrollTo({top:document.body.scrollHeight,behavior: 'smooth'});")
        time.sleep(0.15)
    driver.execute_script("window.scrollTo({top: 0,behavior: 'smooth'});")
    time.sleep(0.15)
    

def _tokopedia_handler(driver):
    #get query from front-end
    product = "ps 5"
    url = "https://www.tokopedia.com/search?st=product&q={}".format(product)
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
    for link in tqdm(productsLinks[:5]):
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

def _get_chrome_option():
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36"
    options = webdriver.ChromeOptions()
    # options.headless = True
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


# download chromedriver.exe and save in same folder with this file.py
driver = webdriver.Chrome(executable_path="chromedriver.exe",options=_get_chrome_option())
result = _tokopedia_handler(driver)
result_df = pd.DataFrame(result)
result_df.to_csv(r"C:\Users\Daffa Barin\MAGANG\Techbros\tokopediaDataScrapper.csv", index=False)