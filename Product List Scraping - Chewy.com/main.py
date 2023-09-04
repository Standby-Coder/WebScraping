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
from util.spider import *

<<<<<<< Updated upstream
=======
import multiprocessing as mp
import threading 
from queue import Queue

>>>>>>> Stashed changes

# # print everything to a file
# import sys
# sys.stdout = open("output.txt", "w")

def get_product_info(url):
    headers = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    spec_info = get_spec(soup)

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


def main(url, df1=None):
    # url = ["https://www.chewy.com/frisco-steel-framed-elevated-dog-bed/dp/139415",
    #         "https://www.chewy.com/american-journey-minced-salmon-tuna/dp/160945",
    #         "https://www.chewy.com/simparica-trio-chewable-tablet-dogs/dp/251350",
            # "https://www.chewy.com/carprofen-generic-caplets-dogs/dp/173410"]

    df2 = pd.DataFrame(
        columns=["item_number", "url", "title", "brand", "advertised_price", "autoship_price", "weight", "desc",
                 "Prescription"])

    next_level = url

    if df1 is None:
        i = 0
    else:
        i = len(os.listdir("./prodlist"))

    product_url_list = []

    try:
        for next_url in next_level:
            if next_url.startswith("https://www.chewy.com"):
                product_url_list, next_level_list = spider(next_url, [])
                print("URL = ", next_url)
            else:
                product_url_list, next_level_list = spider("https://www.chewy.com" + next_url, [])
                print("URL = ", "https://www.chewy.com" + next_url)

            print("Product List Length = ", len(product_url_list))
            print("Next Length = ", len(next_level_list))

            for j in tqdm(product_url_list):
                if j.startswith("https://www.chewy.com"):
                    prod_info = get_product_info(j)
                else:
                    prod_info = get_product_info("https://www.chewy.com" + j)
                if prod_info["item_number"] == "":
                    continue

                if df1 is not None:
                    if prod_info["item_number"] in df1["item_number"].values:
                        continue

                if prod_info["item_number"] in df2["item_number"].values:
                    continue

<<<<<<< Updated upstream
                # df2 = df2.append(prod_info, ignore_index=True
                df2 = pd.concat([df2, pd.DataFrame(prod_info, index=[0])], ignore_index= True)

            for j in next_level_list:
                if j not in next_level:
                    next_level.append(j)
=======
                df = pd.concat([df, pd.DataFrame(prod_info, index = [0])], ignore_index = True)
            
            # for j in next_level_list:
            #     if j not in next_level:
            #         next_level.append(j)
>>>>>>> Stashed changes

            print("Next Level Length = ", len(next_level))

            if len(df2) > 100:
                df2.to_csv(f"./prodlist/product_info_{i}.csv", index=False)
                df2 = pd.DataFrame(
                    columns=["item_number", "url", "title", "brand", "advertised_price", "autoship_price", "weight",
                             "desc", "Prescription"])
                i = i + 1
    except Exception as e:
        print("Unexpected error, dumping current df......")
        df2.to_csv(f"./prodlist/product_info_{i}.csv", index=False)
        print(e)

    df2.to_csv(f"./prodlist/product_info_{i}.csv", index=False)


def debug(url):
    headers = ({'User-Agent':
                    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
                'Accept-Language': 'en-US, en;q=0.5'})
    response = requests.get(url, headers=headers)
    soup = bs4.BeautifulSoup(response.text, "html.parser")
    # info = soup.find("div", attrs={"data-event-label" : "product-detail-description"})
    # head = info.find(lambda tag:tag.name == "h3" and "Details" in tag.text)
    # div = head.find_next("div")
    # desc = div.find("p")
    for a in soup.find_all('a', href=True):
        if re.search("/dp/", a['href']):
            print(a['href'])


def combine_df(mode="save"):
    df = pd.DataFrame(
        columns=["item_number", "url", "title", "brand", "advertised_price", "autoship_price", "weight", "desc",
                 "Prescription"])

    # list of csv files named as product_info
    csv_list = os.listdir("./prodlist")
    csv_list = [i for i in csv_list if i.startswith("product_info")]
    csv_list.sort()

    for csv in csv_list:
<<<<<<< Updated upstream
        df = pd.concat([df,pd.read_csv(f"./prodlist/{csv}")], ignore_index= True)
=======
        df = pd.concat([df, pd.read_csv("./prodlist/" + csv)], ignore_index = True)
>>>>>>> Stashed changes

    if mode == "save":
        df.to_csv("./prodlist/product_info.csv", index=False)
    elif mode == "return":
        return df


if __name__ == "__main__":
    start_url = ["/", "/carprofen-generic-caplets-dogs/dp/173410"]

    df = None
    if os.path.exists("./prodlist"):
        df = combine_df(mode="return")

    main(start_url, df)
    # debug("https://www.chewy.com/b/birthday-shop-2700")
    # debug("https://www.chewy.com/simparica-trio-chewable-tablet-dogs/dp/251350")
    # debug("https://www.chewy.com/american-journey-minced-salmon-tuna/dp/160945")
