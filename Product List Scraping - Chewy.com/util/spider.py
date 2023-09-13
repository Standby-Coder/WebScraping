import requests
import bs4
import re

def get_product_urls(soup):
    product_url_list = []
    next_level_list = []

    for a in soup.find_all('a', href=True):
        if re.search("chewy.ms.tagdelivery.com", a['href']):
            continue
        
        if re.search("/dp/", a['href']):
            if a['href'].startswith("https://www.chewy.com") or a['href'].startswith("/"):
                product_url_list.append(a['href'])
                
        elif re.search("/b/", a['href']):
            next_level_list.append(a['href'])

    product_url_list = list(set(product_url_list))
    next_level_list = list(set(next_level_list))

    return product_url_list, next_level_list

def spider(url, next_level_list):
    headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    
    product_url_list_new, next_level_list_new = [] , []

    for i in url:
        response = requests.get(url, headers = headers)
        soup = bs4.BeautifulSoup(response.text, "html.parser")

        product_url_list_new, next_level_list_new = get_product_urls(soup)
        

    product_url_list_new = list(set(product_url_list_new))
    next_level_list_new = list(set(next_level_list_new))

    return product_url_list_new, next_level_list_new