

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time

cleat_data=pd.DataFrame(columns=['Collection','Name','Price','Color/Color Status'])


url='https://www.adidas.com/us/men-athletic_sneakers'

#step 1 - get data from the site
browser=webdriver.Chrome(service=Service('C:/Users/eltou/Downloads/chromedriver_win32/chromedriver.exe'))
browser.get(url)

pageHeight=6000
scroll=0

while scroll < pageHeight:
    scroll=scroll+60
    time.sleep(0.01)
    browser.execute_script('document.documentElement.scrollTop=' + str(scroll))


page_object=browser.execute_script('return document.body.innerHTML')

#step 2 - parse data
parsed_object=BeautifulSoup(page_object,'html.parser')

#step 3 - find relevant data elements
elements=parsed_object.find_all('div',class_='grid-item')


#step 4 - iterate through all data elements
for shoe in elements:
    collection=shoe.find('p',class_='gl-paragraph gl-paragraph--s glass-product-card__category').text
    name=shoe.find('p',class_='gl-paragraph gl-paragraph--s glass-product-card__title').text
    color = shoe.find('p',class_= 'gl-paragraph gl-paragraph--s glass-product-card__label').text
    try:
        price=shoe.find('div',class_='gl-price-item notranslate').text
    except:
        price=shoe.find('div',class_= 'gl-price-item gl-price-item--sale notranslate').text
        continue
    tinydf=pd.DataFrame(columns=['Collection','Name','Price', 'Color/Color Status'],data=[[collection,name,price,color]])
    cleat_data=cleat_data.append(tinydf)
    

pd.set_option('display.max_columns', None)
print(cleat_data.head(-20))
    
cleat_data.to_excel('C:/Users/eltou/Downloads/seleniumScraping.xlsx')  