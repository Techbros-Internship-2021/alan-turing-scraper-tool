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

import re

class linkFactory:
    
    def __init__(self, user_query):
        self.query = user_query

    def _shopee_link_factory(self):
        
        def generate_odd_numbers(length_num):
            odd_number = []
            for i in range(10):
                if i%2 == 1:
                    odd_number.append(i)
            return odd_number[:length_num]

        def preprocess_list(my_list):
            my_list_new = []
            for elem in my_list:
                num_spaces = 0
                elem_list = elem.split(' ')
                for (idx, char_elem) in enumerate(elem):
                    if char_elem == ' ':
                        num_spaces+=1
                        
                if num_spaces > 0:
                    assert len(elem_list) - num_spaces == 1
                    list_odd_num = generate_odd_numbers(num_spaces)
                    for odd_num in list_odd_num:
                        elem_list.insert(odd_num, '%20')
                    elem = ''.join(elem_list)
                my_list_new.append(elem)
            return my_list_new
        
        normal_search = f'https://shopee.co.id/search?keyword='

        if self.query['Product Name']:
            product_name = self.query['Product Name'].split(' ')
            product_link = f'{product_name[0].lower()}'
            if len(product_name) > 1:
                for x in product_name[1:]:
                    _link = f'%20{x.lower()}'
                    product_link += _link
            
            normal_search += product_link

        if self.query['Location']:
            loc_list = preprocess_list(self.query['Location'])
            print('[INFO] loc_list:', loc_list)
            loc_link = f'&locations={loc_list[0]}'
            if len(loc_list) > 1:
                for x in loc_list[1:]:
                    _link = f'%2C{x}'
                    loc_link += _link
                    
            normal_search += loc_link
        
        normal_search += f'&noCorrection=true'

        if self.query['Official Store']:
            normal_search += f'&officialMall=true'
        
        if self.query['Order']:
            if self.query['Order'] == 'Ascending':
                normal_search += f'&order=asc&page=0'
            else:
                normal_search += f'&order=desc&page=0'

        if self.query['Rating']:
            _rating = self.query['Rating']
            normal_search += f'&ratingFilter={_rating}'
            
        if self.query['Order']:
            normal_search += f'&sortBy=price'
        else:
            if self.query['Relevance']:
                normal_search += f'&sortBy=relevancy'
            else:
                if self.query['Latest']:
                    normal_search += f'&sortBy=ctime'

        return normal_search

    def _blibli_link_factory(self):
        
        normal_search = f'https://www.blibli.com/cari/'

        if self.query['Product Name']:
            product_name = self.query['Product Name'].split(' ')
            for i in range (len(product_name)):
                normal_search += product_name[i].lower()
                if i != len(product_name)-1:
                    normal_search += '%20'

        if self.query['Rating']:
            _rating = self.query['Rating']
            normal_search += f'?rating={_rating}'
    # Choose 1 filter
        if self.query['Order'] == 'Ascending':
            normal_search += f'&sort=3'
        elif self.query['Order'] == 'Descending':
            normal_search += f'&sort=4'
        elif self.query['Relevance']:
            normal_search += f'&sort=0'
        elif self.query['Latest']:
            normal_search += f'&sort=1'

        if self.query['Official Store']:
            normal_search += f'&seller=Official%20Store'
        
        if self.query['Location']:
            location = self.query['Location']
            for i in range(len(location)):
                normal_search +=  '&location='
                loc = location[i]
                splittedloc = loc.split()
                for j in range(len(splittedloc)):
                    normal_search +=  splittedloc[j]
                    if j != len(splittedloc)-1:
                        normal_search +=  '%20'
        
        return normal_search

class shopeeUtilities:
    def __init__(self, soup):
        # soup: html elements from product page
        self.soup = soup
    
    def get_product_name(self):
        product_name = self.soup.find_all('div',{'class':'flex flex-auto _3-GQHh'})
        product_name = product_name[0].find_all('span')[0].get_text(separator=" ").strip() if len(product_name) > 0 else None
        return product_name
    
    def get_product_rating(self):
        product_rating = self.soup.find_all('div',{'class':'flex _3A3c6_'})
        if len(product_rating) > 0:
            product_rating = product_rating[0].find_all('div',{'class':'OitLRu _1mYa1t'})[0]
            product_rating = float(product_rating.get_text(separator=" ").strip())
        else:
            product_rating = None
        return product_rating

    def get_product_num_review(self):
        num_review = self.soup.find_all('div',{'class':'flex _3A3c6_'})
        if len(num_review) > 0:
            num_review = num_review[1].find_all('div',{'class':'OitLRu'})[0]
            num_review = num_review.get_text(separator=" ").strip()
        else:
            num_review = None
        return num_review

    def get_product_num_sold(self):
        num_sold = self.soup.find_all('div',{'class':'flex _210dTF'})
        if len(num_sold) > 0:
            num_sold = num_sold[0].find_all('div',{'class':'aca9MM'})[0]
            num_sold = num_sold.get_text(separator=" ").strip()
        else:
            num_sold = None
        return num_sold

    def get_product_price(self):
        price_text = self.soup.find_all('div',{'class':'_3e_UQT'})
        if len(price_text) > 0:
            price_text = price_text[0].get_text(separator=" ").strip().split('-')[-1]
            price_text = re.findall("[0-9]", price_text)
            price_text = ''.join(price_text)
            price_text = float(price_text)
        else:
            price_text = None
        return price_text
    
    def get_product_spec(self): 
        specs_dict = dict()
        product_spec_div = self.soup.find_all('div',{'class':'aPKXeO'})
        if len(product_spec_div) > 1:
            product_spec_div = product_spec_div[1:]
            for product_spec_text in product_spec_div:
                spec_key = product_spec_text.find_all('label',{'class':'SFJkS3'})[0].text.strip()
                spec_value =  product_spec_text.find_all('div')[0].text.strip()
                specs_dict.update({str(spec_key):spec_value})
        else:
            specs_dict = None
        return specs_dict

    def get_product_category(self):
        product_category_list = []
        product_category_div = self.soup.find_all('a',{'class':'_3YDLCj _3LWINq'})
        if len(product_category_div) > 0:
            for product_category_text in product_category_div:
                product_category = product_category_text.text.strip()
                product_category_list.append(product_category)
            product_category_list = product_category_list[-2]
        else:
            product_category_list = None
        return product_category_list

    def get_product_images_link(self):
        product_image_div = self.soup.find_all('div',{'class':'_12uy03 _2GchKS'})
        product_image_url = product_image_div[0].get('style') if len(product_image_div) > 0 else None
        print('[INFO] product_image_url:', product_image_url)
        print('[INFO] type(product_image_url):', type(product_image_url))
        product_image_url = re.findall('(?:(?:https?|ftp):\/\/)?[\w/\-?=%.]+\.[\w/\-&?=%.]+', product_image_url)[0]
        return product_image_url

    def get_store_name(self):
        store_name_div = self.soup.find_all('div',{'class':'_3uf2ae'})
        store_name_text = store_name_div[0].text.strip() if len(store_name_div) > 0 else None
        return store_name_text

    def get_store_response_duration(self):
        store_response_duration_div = self.soup.find_all('span',{'class':'zw2E3N'})
        store_response_duration_text = store_response_duration_div[3].text.strip() if len(store_response_duration_div) > 0 else None
        return store_response_duration_text

    def get_store_follower(self): 
        store_follower_div = self.soup.find_all('span',{'class':'zw2E3N'})
        store_follower = store_follower_div[5].text.strip() if len(store_follower_div) > 0 else None
        return store_follower
