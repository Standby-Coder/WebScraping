import requests
import bs4
import re

# def get_product_urls(soup):
#     product_url_list = []
#     for a in soup.find_all('a', href=True):
#         if re.search("https://www.chewy.com/", a['href']):
#             product_url_list.append(a['href'])
    
#     product_url_list = list(set(product_url_list))

#     # seperate those which contains "/dp/[0-9]*" and those which don't
#     product_url_list_1 = []
#     product_url_list_2 = []
#     for url in product_url_list:
#         if re.search("/dp/[0-9]*", url):
#             product_url_list_1.append(url)
#         else:
#             product_url_list_2.append(url)

#     return product_url_list_1, product_url_list_2

# def spider(url):
#     headers = ({'User-Agent':
#             'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
#             'Accept-Language': 'en-US, en;q=0.5'})
#     response = requests.get(url, headers = headers)
#     soup = bs4.BeautifulSoup(response.text, "html.parser")
    
#     product_url_list, next_level_list = get_product_urls(soup)

#     return product_url_list, next_level_list

# create a web spider which can crawl through the website and get all the product urls which are listed on the website

def get_product_urls(soup):
    product_url_list = []
    next_level_list = []
    for a in soup.find_all('a', href=True):
        if re.search("/dp/", a['href']):
            if a['href'].startswith("https://www.chewy.com") or a['href'].startswith("/"):
                product_url_list.append(a['href'])
        elif re.search("/b/", a['href']) or re.search("/brands/", a['href']):
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