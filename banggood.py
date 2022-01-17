# https://www.banggood.com/

from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re
import datetime

s = HTMLSession()

url = 'https://www.banggood.com/Flashdeals.html?bid=35138&from=nav'

r = s.get(url)

r.html.render(scrolldown=2, sleep=6)
# r.html.render(sleep=2)

soup = BeautifulSoup(r.html.html, 'html.parser')

products = soup.find_all(class_="product-item")

# print(len(products))
products_infos = []

try:
    for product in products:
        title = product.find('a', {'class': 'products_name'})
        link = product.find('a', {'class': 'p-img'})
        url = link['href']
        new_title = title.text.strip()
        price = product.find('p', {'class': 'price'})
        price_old = product.find('span', {'class': 'pre_price'})
        price_rebate = product.find('span', {'class': 'off'})
        progress = product.find_next('div', {'class': 'sold-progress'})
        sold = product.find('p', {'class': 'sold-num'})
        timer = product.find('span', {'class': 'count-time'})
        remaining_time = timer['data-time']

        the_product = {
            'title': new_title,
            'url': url,
            'price_reel': price.text,
            'price_old': price_old.text,
            'price_rebate': price_rebate.text,
            #'progress': type(progress),
            'sold': sold.text,
            'timer': remaining_time,
            # 'remaining_time': datetime.timedelta(seconds=remaining_time),
            # 'date_today': datetime.datetime.now()
        }

        products_infos.append(the_product)
        
except:
    pass

print(products_infos)
print(len(products_infos))