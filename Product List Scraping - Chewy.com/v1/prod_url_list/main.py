import numpy as np
import re
import gc
import os
import requests
import lxml
import bs4

from tqdm import tqdm

import threading

def spider(next_url, traversed):
    headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    
    prodlist_new = np.array([], dtype = object)
    next_level_new = np.array([], dtype = object)
    next_list = np.array([], dtype = object)

    response = requests.get(next_url, headers = headers)
    soup = bs4.BeautifulSoup(response.text, "lxml")
    
    new = np.array(list(map(lambda a: a['href'], soup.find_all('a', href=True))))
    new = np.array(list(filter(lambda a: not re.search("chewy.ms.tagdelivery.com", a), new)))
    
    prodlist_new = np.array(list(filter(lambda a: re.search("/dp/", a), new)))
    
    next_level_new = np.array(list(filter(lambda a: re.search("/b/", a), new)))


    prodlist_new = np.unique(prodlist_new)
    
    for i in next_level_new:
        if i not in traversed:
            next_list = np.append(next_list, i)
        
    return prodlist_new, next_list

def spider2(next_url, traversed):

    headers = ({'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US, en;q=0.5'})
    
    prodlist_new = np.array([], dtype = object)
    next_level_new = np.array([], dtype = object)
    next_list = np.array([], dtype = object)

    response = requests.get(next_url, headers = headers)
    soup = bs4.BeautifulSoup(response.text, "lxml")
    # Get all product links parallely
    threads = []
    for i in soup.find_all('a', href=True):
        if re.search("/dp/", i['href']):
            t = threading.Thread(target = prodlist_new.append(i['href']))
            threads.append(t)
            t.start()
        if re.search("/b/", i['href']):
            t = threading.Thread(target = next_level_new.append(i['href']))
            threads.append(t)
            t.start()
    
    for t in threads:
        t.join()
    
    prodlist_new = np.unique(prodlist_new)
    
    for i in next_level_new:
        if i not in traversed:
            next_list = np.append(next_list, i)
        
    return prodlist_new, next_list

def main(traversed, prodlist, next_level):
    while len(next_level) != 0:
        try:
            if next_level[0] in traversed:
                next_level = np.delete(next_level, 0)
                continue

            if next_level[0].startswith("/"):
                next_level[0] = "https://www.chewy.com" + next_level[0]

            if next_level[0].startswith("hhttps://"):
                next_level[0] = next_level[0].replace("hhttps://", "https://")

            if next_level[0].startswith("("):
                next_level[0] = next_level[0].replace("(", "")
                next_level[0] = next_level[0].replace(")", "")
            
            prodlist_new, next_list = spider(next_level[0], traversed)
            prodlist = np.append(prodlist, prodlist_new)
            traversed = np.append(traversed, next_level[0])
            next_level = np.append(next_level, next_list)
            next_level = np.delete(next_level, 0)
            next_level = np.unique(next_level)
            gc.collect()
            if prodlist.shape[0] % 1000 == 0:
                print("Traversed: ", len(traversed))
                print("Product Urls: ", len(prodlist))
                print("Next Level: ", len(next_level))
        except:
            print("URL: ", next_level[0])
            print("Connection refused by the server..Retrying")
    return traversed, prodlist, next_level

if __name__ == "__main__":
    traversed = np.array([], dtype = object)
    prodlist = np.array([], dtype = object)
    next_level = np.array(["/"], dtype = object)
    x, y, z = main(traversed, prodlist, next_level)
    with open("prod_url_list_traversed.txt", "w") as f:
        for i in x:
            f.write(i + "\n")
    
    with open("prod_url_list_prodlist.txt", "w") as f:
        for i in y:
            f.write(i + "\n")