import re
import gc
import os
import sys
import bs4
import requests
import datetime as dt
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

from tqdm import tqdm
from util.get_product_details import *
from util.spiderv2 import *

import multiprocessing as mp
import lxml
import time

def get_product_info(url, df, items_traversed):
    headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0',
            'Accept-Language': 'en-US, en;q=0.5'})
    
    if url.startswith("/"):
        url = "https://www.chewy.com" + url

    print("Scraping: " + url)
    while True:
        try:
            response = requests.get(url, headers = headers)
            break
        except:
            print("Connection refused by the server..Retrying")
            time.sleep(3)
            continue

    soup = bs4.BeautifulSoup(response.text, "html.parser")

    if check_prescription(soup) == False:
        return None

    spec_info = get_spec(soup)

    if spec_info["item_number"] is None or spec_info["item_number"] == "" or spec_info["item_number"] in items_traversed:
        return None
    
    if df is not None and url in df["url"].values:
        return None

    product_info = {}
    
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

def main(start_url, df, traversed, items_traversed, path):
    next_level = start_url
    traversed = np.array([], dtype = object)

    nextl = np.array([], dtype = object)

    try:    
        for next_url in tqdm(next_level):

            if(next_url.startswith("/")):
                next_url = "https://www.chewy.com" + next_url
                
            if next_url.startswith("hhttps://"):
                next_url = next_url.replace("hhttps://", "https://")

            print("\nCrawling: " + next_url)
            traversed = np.append(traversed, next_url)
            
            start = time.time()
            product_url_list, next_level_list = spider(next_url, traversed)
            print("Spider Time taken: " + str(time.time() - start))
                
            start = time.time()
            with mp.Pool(processes = 8) as pool:
                product_info = pool.starmap(get_product_info, [(i, df, items_traversed) for i in product_url_list])

            for prod_info in product_info:
                    
                if prod_info is None:
                    continue
                
                if prod_info["item_number"] == "":
                    continue
            
                if prod_info["item_number"] not in items_traversed: 
                    items_traversed = np.append(items_traversed, prod_info["item_number"])
                    df = pd.concat([df, pd.DataFrame(prod_info, index = [0])], ignore_index = True)

                if len(df) > 1000:
                    x = len(os.listdir(path))
                    df.to_csv( path + f"/{x}.csv", index = False)
                    df = pd.DataFrame(columns = ["item_number", "url", "title", "brand", "advertised_price", "autoship_price", "weight", "desc", "Prescription"])
                    gc.collect()

            print("Product Info Time taken: " + str(time.time() - start))

            if(len(next_level_list) == 0):
                return df
            
            nextl = np.append(nextl, next_level_list)
            nextl = np.unique(nextl)
        
        next_level = nextl
        print("Total Scraped till now: ", len(df))
        df = main(next_level, df, traversed, items_traversed, path)
    except:
        with open("traversed.txt", "w") as f:
            for url in traversed:
                f.write(url + "\n")
        x = len(os.listdir(path))
        df.to_csv(path + f"/{x}.csv", index = False)
        print("Unexpected error:", sys.exc_info())
        sys.exit(0)
    
    return df    

# def debug():
#     url = "https://www.chewy.com/frisco-steel-framed-elevated-dog-bed/dp/139415"
#     start = time.time()
#     prod_info = get_product_info(url, None)
#     print_product_info(prod_info)
#     print("Time taken: " + str(time.time() - start))

if __name__ == '__main__':
    start_url = np.array(["/"], dtype = object)
    traversed = np.array([], dtype = object)
    items_traversed = np.array([], dtype = object)
    df = pd.DataFrame(columns = ["item_number", "url", "title", "brand", "advertised_price", "autoship_price", "weight", "desc", "Prescription"])
    
    path = "./prodlist/" + str(dt.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))
    os.makedirs(path, exist_ok = True)

    start = time.time()
    df = main(start_url, df, traversed, items_traversed, path)
    print("Total Time elapsed: " + str(time.time() - start))
    x = len(os.listdir(path))
    df.to_csv(path + f"/{x}.csv", index = False)
