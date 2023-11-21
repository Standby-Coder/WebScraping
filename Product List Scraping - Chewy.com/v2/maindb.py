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
from mysql import connector

from tqdm import tqdm
from util.get_product_details import *
from util.spiderv2 import *

import multiprocessing as mp
import lxml
import time

def update_db(p, b):
    host = "127.0.0.1"
    user = "keshav"
    password = "123456"
    database = "chewy"

    conn = connector.connect(host=host, user=user, password=password, database=database)
    cursor = conn.cursor()

    cursor.execute("INSERT IGNORE into products2 values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", 
                   (p['title'], p['url'], p['brand'], p['advertised_price'], p['autoship_price'], p['weight'], p['desc'], p['item_number'], p['Prescription'], b))
    conn.commit()
    cursor.close()
    conn.close()

def get_product_info(url, df, batch):
    headers = ({'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/101.0.0.0',
            'Accept-Language': 'en-US, en;q=0.5'})
    
    if url.startswith("/"):
        url = "https://www.chewy.com" + url

    print("Scraping: " + url)
    
    while(True):
        try:
            response = requests.get(url, headers = headers)
            break
        except:
            print("Connection refused by the server..")
            print("Retrying after 5 seconds..")
            time.sleep(5)
            continue
    
    soup = bs4.BeautifulSoup(response.text, "html.parser")

    spec_info = get_spec(soup)

    # if spec_info["item_number"] is None or spec_info["item_number"] == "":
    #    return None

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

    update_db(product_info, batch)

def main(df, batch):
    for url in tqdm(df["url"].values):
        get_product_info(url, df, batch)

if __name__ == "__main__":
    host = "127.0.0.1"
    user = "keshav"
    password = "123456"
    database = "chewy"

    conn = connector.connect(host=host, user=user, password=password, database=database)
    df = pd.read_sql("select url from prod_urls2", conn)
    conn.close()
    print(df.shape)
    x = input("Start from: ")
    y = input("End at: ")
    batch = input("Enter batch to safe delete: ")
    df = df.iloc[int(x):int(y)]

    main(df, batch)
    print("-----------------------------------------------------------\n\nPlease check the database for the results, batch number = " + batch)