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

def getFilter(driver):
    #official store
    driver.find_element(By.XPATH, "//div[contains(@name,'official')]").click()

    # rating 4 keatas
    driver.find_element(By.XPATH, "//div[contains(@value,'4 Keatas')]").click()

    #lokasi
    driver.find_element(By.XPATH, "//a[contains(@class,'css-wz9tp9-unf-link en8iawh0')]").click()
    driver.find_element(By.XPATH, "//span[contains(text(),'Reset')]").click()
    lokasi = input("lokasi mana?")
    driver.find_element(By.XPATH, "//div[contains(@value,'{}')]".format(lokasi)).click()
    driver.find_element(By.XPATH, "//span[contains(text(),'Terapkan')]").click()


def popUpHandler(driver):
    time.sleep(0.1)
    try:
        driver.find_element(By.XPATH, "//div[contains(@class,'unf-coachmark__action-wrapper css-1xhj18k ety06v13')]").click()
    except:
        print("Removed area request pop-up")
    time.sleep(0.1)
    try :
        driver.find_element(By.XPATH, "//div[contains(@class,'css-13qaojv ek4e0y61')]").click()
    except:
        print("Removed merchant pro pop-up")
    
def getListOfLink(driver):
    product_info_list = driver.find_elements_by_class_name('css-y5gcsw')
    productLinks = []
    for findlink in product_info_list:
        a = findlink.find_element_by_tag_name('a')
        productLinks.append(a.get_property('href'))
    return productLinks

def scrolling(driver):
    for i in range(10):
        driver.execute_script("window.scrollTo({top:document.body.scrollHeight,behavior: 'smooth'});")
        time.sleep(0.15)
    driver.execute_script("window.scrollTo({top: 0,behavior: 'smooth'});")
    time.sleep(0.15)
    
def contentScrapper(driver,listOfLink):
    ListOfdetails = []
    listOfLink = [x for x in listOfLink if not x.startswith("https://ta.tokopedia.com/")]
    for link in tqdm(listOfLink[:20]):
        driver.get(link)
        try:
            time.sleep(1)
            productName = driver.find_element(By.XPATH, "//h1[contains(@class,'css-1wtrxts')]").text
        except:
            continue
        scrolling(driver)
        productPrice = driver.find_element(By.XPATH, "//div[contains(@class,'price')]").text
        try:
            productRate = driver.find_element(By.XPATH, "//h5[contains(@class,'css-zeq6c8')]").text
        except:
            productRate = "Belum ada rate"
        try:
            productReview = driver.find_element(By.XPATH, "//p[contains(@class,'css-roiplm-unf-heading-unf-heading e1qvo2ff8')]").text
        except:
            productReview = "Belum ada review"
        try:
            producStock = driver.find_element(By.XPATH, "//p[contains(@data-testid,'stock-label')]").text
        except:
            producStock = "Ada beberapa varian"
        try:
            productSold = driver.find_element(By.XPATH, "//div[contains(@data-testid,'lblPDPDetailProductSoldCounter')]").text
        except:
            productSold = "Belum ada produk terjual"
        productImage = driver.find_element(By.XPATH, "//div[contains(@class,'css-19i5z4j')]/img").get_attribute("src")
        productStore = productStore = driver.find_element_by_xpath("//*//div/a/h2").text
        productCondition = driver.find_element_by_xpath("//ul[@data-testid='lblPDPInfoProduk']/li[1]/span[2]").text
        storeRating = driver.find_element_by_xpath("//div[@class='css-1w2cnd1']/div[1]/div[1]").text
    #         storeLocation
    #         processTime
    #         storeLink
        productDetails = {"Product Name" : productName, "Product Price" :productPrice, "Product Rate" : productRate,
                        "Product Review" : productReview, "Product Sold": productSold, "Product Stock" : producStock,
                        "Product Condition" :productCondition, "Product Store": productStore, "Store Rating": storeRating,
                        "Product Image": productImage}
        ListOfdetails.append(productDetails)
    return ListOfdetails

def initiate():
    options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36'
    options.add_argument('user-agent={0}'.format(user_agent))
    driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
    wait = WebDriverWait(driver, 20)
    action = ActionChains(driver)
    driver.maximize_window()
    driver.get("https://www.tokopedia.com/")
    time.sleep(3)
    product = input("Keyword")
    driver.find_element(By.XPATH, "//input[contains(@class,'css-ubsgp5 e16vycsw0')]").send_keys(product)
    driver.find_element(By.XPATH, "//button[contains(@class,'css-1czin5k e1v0ehno1')]").click()
    time.sleep(1)
    popUpHandler(driver)
    scrolling(driver)
    popUpHandler(driver)
    listOfLink = getListOfLink(driver)
    results = contentScrapper(driver,listOfLink=listOfLink)
    results_df = pd.DataFrame(results)
    results_df.to_csv(r"C:\Users\Daffa Barin\tokopediaDataScrapper.csv", index=False)

initiate()