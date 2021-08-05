import pandas as pd
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


def get_link_product_per_page(driver,NumofPage):
	listLinkofproduct = []
	page = 0
	for page in range(NumofPage):
	    Product_info_list = driver.find_elements_by_class_name('bl-thumbnail--slider')
	    for findlink in Product_info_list:
	        a = findlink.find_element_by_tag_name('a')
	        listLinkofproduct.append(a.get_property('href'))
	    print("[INFO] page: {}; recorded product num: {}".format(page+1, len(listLinkofproduct)))
	    driver.find_element(By.XPATH, "//a[contains(@class,'bl-pagination__next')]").click()
	return listLinkofproduct

def get_spec(prod_specs):
    spec = []
    for sp in prod_specs:
        spec.append(sp.text)
    return spec

def get_picture(driver, prod_picture):
    links = []
    for  link in prod_picture:
        links.append(link.get_attribute('src'))
    if len(links)==0:
        image = driver.find_elements(By.XPATH, "//div[contains(@class,'c-carousel-mv c-product-gallery__main')]/*[name()=('div')]/*[name()=('div')]/*[name()=('div')]/*[name()=('div')]/*[name()=('div')]/*[name()=('div')]/*[name()=('picture')]/*[name()=('img')]")
        return(image[0].get_attribute('src'))
    else:
        return links

def get_product_data(driver,listLinkofproduct):
	detailsData = []
	for link in tqdm(listLinkofproduct):
	    driver.get(link)
	    np = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[1]/div[1]/h1').text
	    pp = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[2]/div/div[1]/div/span').text
	    sp = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[3]').text
	    rate = driver.find_element_by_xpath('//*[@id="section-ulasan-barang"]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/span').text
	    cp = driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[1]/div').text
	    spec = get_spec(driver.find_elements(By.XPATH, "//table[contains(@class,'c-information__table')]/*[name()=('tbody')]/*[name()=('tr')]"))
	    prod_picture = get_picture(driver, driver.find_elements(By.XPATH, "//div[contains(@class,'c-product-gallery__thumbnails')]/*[name()=('div')]/*[name()=('div')]/*[name()=('picture')]/*[name()=('img')]"))
	    storeP = driver.find_element_by_xpath('//*[@id="section-informasi-pelapak"]/div[2]/div/div[1]/div[1]/h3/a').text
	    PlaceP = driver.find_element_by_xpath('//*[@id="section-informasi-pelapak"]/div[2]/div/div[1]/div[1]/a').text
	    review = driver.find_element_by_xpath('//*[@id="section-ulasan-barang"]/div[2]/div/div[1]/div[1]/div[1]/div[2]/p').text
	    soldP = driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[1]/div[1]/div/span').text
	    process = driver.find_element_by_xpath('//*[@id="section-informasi-pelapak"]/div[2]/div/div[2]/div[2]/h3').text
	    storeFeedBScore = driver.find_element_by_xpath('//*[@id="section-informasi-pelapak"]/div[2]/div/div[2]/div[1]/div[1]/div/span').text
	    listofitems = {
	        'Product name':np,'Product price':pp,'Prod Review':review,
	        'Product Rate': rate,'Product stock':sp,'Product condition':cp,
	        'Product Picture':prod_picture,'Product Specs':spec,'sold':soldP,'Store Name':storeP, 
	        'Store Location':PlaceP,'Process Time': process, 'Store Feedback Score': storeFeedBScore,
	        'Product Link': link
	    }
	    detailsData.append(listofitems)
	    driver.implicitly_wait(10)

	return detailsData

def bukalapak_product_link(product):
	driver = webdriver.Chrome(ChromeDriverManager().install())
	driver.maximize_window()
	driver.get("https://www.bukalapak.com/")

	# value = input("keywords: ")
	time.sleep(0.5)
	driver.find_element(By.XPATH, "//input[contains(@id,'search')]").send_keys(product)
	driver.find_element(By.XPATH, "//button[contains(@class,'v-omnisearch__submit')]").click()
	screen_height = driver.execute_script("return window.screen.height;")
	i = 0
	while True:
	    driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))  
	    i += 1
	    time.sleep(1)
	    scroll_height = driver.execute_script("return document.body.scrollHeight;")  
	    if (screen_height) * i > scroll_height/2:
	        break 
	time.sleep(0.5)
	driver.find_element(By.XPATH, "//span[text()='4 ke atas']").click()
	driver.find_element(By.XPATH, "//*[@id='product-explorer-container']/div/div[1]/div[1]/div/div[2]/div[1]/div/label[3]/span[2]/span").click()
	# NumofPage = int(input("Number of page: "))
	time.sleep(5)
	link_of_product = get_link_product_per_page(driver,1)
	data_result = get_product_data(driver,link_of_product)
	
	data_result_df = pd.DataFrame(data_result)
	data_result_df.to_csv(r"C:\Users\User\Documents\Techbros Internship\projects\bukalapak_data_scraper.csv", index=False)

bukalapak_product_link("laptop")