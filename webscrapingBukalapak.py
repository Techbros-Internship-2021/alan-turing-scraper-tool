import pandas as pd
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

class Bukalapak:
	"""docstring for Bukalapak"""
	def __init__(self, numofpage, keywords):
		# super(Bukalapak, self).__init__()
		self.numofpage = numofpage
		self.keywords = keywords
		self.driver = webdriver.Chrome(ChromeDriverManager().install())
		self.driver.maximize_window()
		self.driver.get("https://www.bukalapak.com/")
		self.driver.find_element(By.XPATH, "//input[contains(@id,'search')]").send_keys(self.keywords)
		self.driver.find_element(By.XPATH, "//button[contains(@class,'v-omnisearch__submit')]").click()
		self.driver.find_element(By.XPATH, "//span[text()='4 ke atas']").click()
		self.driver.find_element(By.XPATH, "//*[@id='product-explorer-container']/div/div[1]/div[1]/div/div[2]/div[1]/div/label[3]/span[2]/span").click()
		self.product_link, self.allData_product = [], []
			# driver.maximize_window()
			# driver.get("https://www.bukalapak.com/")

	def get_link_(self):
		for page_number in range(self.numofpage):
			Product_info_list = self.driver.find_elements_by_class_name('bl-thumbnail--slider')
			for findlink in Product_info_list:
			    a = findlink.find_element_by_tag_name('a')
			    self.product_link.append(a.get_property('href'))
			print("[INFO] page: {}; recorded product num: {}".format(page_number+1, len(self.product_link)))
			self.driver.find_element(By.XPATH, "//a[contains(@class,'bl-pagination__next')]").click()	

		return self.product_link

	# def get_specification_(product_specification):
	# 	spec = []
	# 	for sp in prod_specs:
	# 	    spec.append(sp.text)
	# 	return spec

	# def get_picture_(self,product_picture):
	#     links = []
	#     for  link in prod_picture:
	#         links.append(link.get_attribute('src'))
	#     if len(links)==0:
	#         image = self.driver.find_elements(By.XPATH, "//div[contains(@class,'c-carousel-mv c-product-gallery__main')]/*[name()=('div')]/*[name()=('div')]/*[name()=('div')]/*[name()=('div')]/*[name()=('div')]/*[name()=('div')]/*[name()=('picture')]/*[name()=('img')]")
	#         return(image[0].get_attribute('src'))
	#     else:
	#         return links

	# def get_dataProduct_(self):
	# 	for j in tqdm(self.get_link_()):
	# 	    self.driver.get(j)
	# 	    np = self.driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[1]/div[1]/h1').text
	# 	    pp = self.driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[2]/div/div[1]/div/span').text
	# 	    sp = self.driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[3]').text
	# 	    rate = self.driver.find_element_by_xpath('//*[@id="section-ulasan-barang"]/div[2]/div/div[1]/div[1]/div[1]/div[1]/div/div/span').text
	# 	    cp = self.driver.find_element_by_xpath('//*[@id="section-informasi-barang"]/div[2]/div[1]/div').text
	# 	    spec = self.get_spec(self.driver.find_elements(By.XPATH, "//table[contains(@class,'c-information__table')]/*[name()=('tbody')]/*[name()=('tr')]"))
	# 	    prod_picture = self.get_picture(self.driver.find_elements(By.XPATH, "//div[contains(@class,'c-product-gallery__thumbnails')]/*[name()=('div')]/*[name()=('div')]/*[name()=('picture')]/*[name()=('img')]"))
	# 	    storeP = self.driver.find_element_by_xpath('//*[@id="section-informasi-pelapak"]/div[2]/div/div[1]/div[1]/h3/a').text
	# 	    PlaceP = self.driver.find_element_by_xpath('//*[@id="section-informasi-pelapak"]/div[2]/div/div[1]/div[1]/a').text
	# 	    review = self.driver.find_element_by_xpath('//*[@id="section-ulasan-barang"]/div[2]/div/div[1]/div[1]/div[1]/div[2]/p').text
	# 	    soldP = self.driver.find_element_by_xpath('//*[@id="section-main-product"]/div[2]/div[1]/div[1]/div/span').text
	# 	    process = self.driver.find_element_by_xpath('//*[@id="section-informasi-pelapak"]/div[2]/div/div[2]/div[2]/h3').text
	# 	    storeFeedBScore = self.driver.find_element_by_xpath('//*[@id="section-informasi-pelapak"]/div[2]/div/div[2]/div[1]/div[1]/div/span').text
	# 	    listofitems = {
	# 	        'Product name':np,'Product price':pp,'Prod Review':review,
	# 	        'Product Rate': rate,'Product stock':sp,'Product condition':cp,
	# 	        'Product Picture':prod_picture,'Product Specs':spec,'sold':soldP,'Store Name':storeP, 
	# 	        'Store Location':PlaceP,'Process Time': process, 'Store Feedback Score': storeFeedBScore,
	# 	        'Product Link': j
	# 	    }
	# 	    self.allData_product.append(listofitems)
	# 	    self.driver.implicitly_wait(10) 
	# 	return self.allData_product

bkl = Bukalapak(numofpage=1,keywords='laptop')
data_scraping = bkl.get_link_()
# df = pd.DataFrame(data_scraping)
# print(df)
print(data_scraping)


