from requests_html import HTMLSession
from bs4 import BeautifulSoup
import re

s = HTMLSession()

url = 'https://www.amazon.ca/gp/goldbox/ref=gbps_ftr_s-6_c86a_wht_30069020?gb_f_deals1=dealTypes:DEAL_OF_THE_DAY%252CBEST_DEAL%252CLIGHTNING_DEAL,sortOrder:BY_SCORE,enforcedCategories:3006902011'

# url = 'https://www.amazon.ca/gp/goldbox/ref=gbps_ftr_s-6_5aeb_wht_30069020?gb_f_deals1=dealTypes:DEAL_OF_THE_DAY%252CBEST_DEAL%252CLIGHTNING_DEAL,sortOrder:BY_SCORE,enforcedCategories:3006902011&pf_rd_p=8a6cc1e9-9881-4806-9377-6cf39b8f5aeb&pf_rd_s=slot-6&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A3DWYIK6Y9EEQB&pf_rd_r=2HQVWCZ18H1KT3T6RYSJ&ie=UTF8'

# url = 'https://www.amazon.ca/gp/goldbox/ref=gbps_ftr_s-6_c86a_enf_30069020?gb_f_deals1=dealTypes:DEAL_OF_THE_DAY%252CBEST_DEAL%252CLIGHTNING_DEAL,sortOrder:BY_SCORE,enforcedCategories:3006902011&pf_rd_p=956ef016-d330-404d-888d-d50717e0c86a&pf_rd_s=slot-6&pf_rd_t=701&pf_rd_i=gb_main&pf_rd_m=A3DWYIK6Y9EEQB&pf_rd_r=RCJSSGTHEDKX11CBM8YT&ie=UTF8#'

r = s.get(url)

r.html.render(sleep=2)

soup = BeautifulSoup(r.html.html, 'html.parser')

# print(soup.prettify())

# products = soup.find('div', id=re.compile('widgetContent'))
# dealview = re.compile('dealview')

# products = soup.find_all('div', attrs={'id': 'dealview'})

products = soup.find_all('div', {'class': 'a-section dealContainer'})

print(len(products))
print(type(products))

all_products = []

for product in products[:6]:

    image_url = product.find('a', {'id': 'dealImage'})


    product_info = {
        'image_url': image_url
    }


    all_products.append(product_info)


print(all_products)