import os
import requests
import json
import bs4
import re
import pandas as pd
import html5lib
import warnings
warnings.filterwarnings("ignore")

from tqdm import tqdm
from util.get_product_details import *
from util.spiderv2 import *

import multiprocessing as mp
import threading 
from queue import Queue

import lxml
import time


def get_product_info(url):
    headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0',
            'Accept-Language': 'en-US, en;q=0.5'})
    response = requests.get(url, headers = headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    
    spec_info = get_spec(soup)

    product_info = {}
    if spec_info["Prescription"] == "Non-Rx":
        return product_info
    
    product_info["url"] = url
    product_info["title"] = get_title(soup)
    product_info["brand"] = get_brand(soup)
    product_info["advertised_price"] = get_advertised_price(soup)
    product_info["autoship_price"] = get_autoship_price(soup)
    product_info["weight"] = spec_info["weight"]
    product_info["desc"] = spec_info["desc"]
    product_info["item_number"] = spec_info["item_number"]
    product_info["Prescription"] = spec_info["Prescription"]

    return product_info

def print_product_info(prod_info):
    print("URL: " + prod_info["url"])
    print("Title: " + prod_info["title"])
    print("Brand: " + prod_info["brand"])
    print("Advertised Price: " + prod_info["advertised_price"])
    print("Autoship Price: " + prod_info["autoship_price"])
    print("Weight: " + prod_info["weight"])
    print("Description: " + prod_info["desc"])
    print("Item Number: " + prod_info["item_number"])
    print("Prescription: " + prod_info["Prescription"])

def main(url, df1 = None):

    df = pd.DataFrame(columns = ["item_number", "url", "title", "brand", "advertised_price", "autoship_price", "weight", "desc", "Prescription"])

    next_level = url

    # if df1 is None:
    i = 0
    # else:
    #     i = len(os.listdir("./prodlist"))

    product_url_list = []

    try:
        start= time.time()
        for next_url in next_level:
            if next_url.startswith("https://www.chewy.com"):
                product_url_list, next_level_list = spider(next_url, [])
                print("URL = " , next_url)
            else:
                product_url_list, next_level_list = spider("https://www.chewy.com" + next_url, [])
                print("URL = " , "https://www.chewy.com" + next_url)
            
            print("Product List Length = " , len(product_url_list))
            print("Next Length = " , len(next_level_list))
            
            for j in tqdm(product_url_list):
                if j.startswith("https://www.chewy.com"):
                    prod_info = get_product_info(j)
                else:
                    prod_info = get_product_info("https://www.chewy.com" + j)
                
                if prod_info == {}:
                    continue
                
                if prod_info["item_number"] == "":
                    continue

                if df1 is not None:
                    if prod_info["item_number"] in df1["item_number"].values:
                        continue
                
                if prod_info["item_number"] in df["item_number"].values:
                    continue

                df = pd.concat([df, pd.DataFrame(prod_info, index = [0])], ignore_index = True)
            
            for j in next_level_list:
                if j not in next_level:
                    next_level.append(j)

            print("Next Level Length = " , len(next_level))

            if len(df) > 100:
                df.to_csv(f"./prodlist/product_info_{i}.csv", index = False)
                df = pd.DataFrame(columns = ["item_number", "url", "title", "brand", "advertised_price", "autoship_price", "weight", "desc", "Prescription"])
                i = i + 1
    except Exception as e:
        print("Unexpected error, dumping current df......")
        df.to_csv(f"./prodlist/product_info_{i}.csv", index = False)
        print(e)

    df.to_csv(f"./prodlist/product_info_{i}.csv", index = False)
    print("Time taken: " + str(time.time() - start))    

def debug(url):
    headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    response = requests.get(url, headers = headers)
    soup = bs4.BeautifulSoup(response.text, "lxml")
    # info = soup.find("div", attrs={"data-event-label" : "product-detail-description"})
    # head = info.find(lambda tag:tag.name == "h3" and "Details" in tag.text)
    # div = head.find_next("div")
    # desc = div.find("p")
    c = 0
    p = []
    for a in soup.find_all('a', href=True):
        if re.search("/dp/", a['href']):
            if a['href'] not in p:
                p.append(a['href'])  
            c = c + 1

    print(p)
    print(len(p))

def combine_df(mode = "save"):
    df = pd.DataFrame(columns = ["item_number", "url", "title", "brand", "advertised_price", "autoship_price", "weight", "desc", "Prescription"])
    csv_list = os.listdir("./prodlist")
    csv_list = [i for i in csv_list if i.startswith("product_info")]
    csv_list.sort()

    for csv in csv_list:
        df = pd.concat([df, pd.read_csv("./prodlist/" + csv)], ignore_index = True)

    if mode == "save":
        df.to_csv("./prodlist/product_info.csv", index = False)
    elif mode == "return":
        return df
    
if __name__ == "__main__":
    start_url = ["/"]

    df = None
    # if os.path.exists("./prodlist"):
    #     df = combine_df(mode = "return")

    main(start_url, df)
    # debug("https://www.chewy.com/")
    # debug("https://www.chewy.com/simparica-trio-chewable-tablet-dogs/dp/251350")
    # debug("https://www.chewy.com/american-journey-minced-salmon-tuna/dp/160945")

