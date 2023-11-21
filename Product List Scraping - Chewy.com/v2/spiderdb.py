from mysql import connector

import numpy as np
import re
import gc
import os
import requests
import lxml
import bs4

from tqdm import tqdm

import threading
import time

def update_db(prodlist, c):
    for i in tqdm(prodlist):
        c.execute(f"INSERT IGNORE INTO prod_urls2 VALUES ('{i}')")
    mydb.commit()

def spider(next_url, traversed, c):
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
    new = np.array(list(filter(lambda a: not re.search("/app/", a), new)))
    new = np.array(list(filter(lambda a: not re.search("#", a), new)))
    new = np.array(list(filter(lambda a: not re.search("tel:", a), new)))
    new = np.array(list(filter(lambda a: not re.search("mailto:", a), new)))
    new = np.array(list(filter(lambda a: re.search("/", a) or re.search("https://www.chewy.com/", a), new)))

    
    prodlist_new = np.array(list(filter(lambda a: re.search("/dp/", a), new)))
    next_level_new = new

    prodlist_new = np.unique(prodlist_new)
    prodlist_new = np.array(list(filter(lambda a: not re.search("chewy.ms.tagdelivery.com", a), prodlist_new)))
    
    t = threading.Thread(target = update_db, args = (prodlist_new, c))
    t.start()
    
    for i in prodlist_new:
        if i.startswith("/"):
            prodlist_new[prodlist_new == i] = "https://www.chewy.com" + i


    for i in next_level_new:
        if i.startswith("http://"):
            next_level_new[next_level_new == i] = i.replace("http://", "https://")
        
        if i.startswith("https://") and not i.startswith("https://www.chewy.com"):
            continue

        if "https://www.chewy.com" + i not in traversed and i not in traversed:
            next_list = np.append(next_list, i)

    return next_list

def main(traversed, next_level, c):
    while len(next_level) != 0:
        try:            
            url = next_level[0]

            if url.startswith("hhttps://"):
                url = url.replace("hhttps://", "https://")
            
            if url.startswith("("):
                url = url.replace("(", "")
                url = url.replace(")","")

            if url.startswith("ttps://"):
                url = url.replace("ttps://","https://")

            if url.startswith("http://"):
                url = url.replace("http://", "https://")

            if not url.startswith("https://www.chewy.com") and not url.startswith("/"):
                print("Invalid URL - ", url)
                url = input("Enter URL or press enter to skip: ")

            if url is None or url == "":
                traversed = np.append(traversed, next_level[0])
                next_level = next_level[1:]
                continue

            if url.startswith("/"):
                url = "https://www.chewy.com" + url
            
            if url.startswith("https://") and not url.startswith("https://www.chewy.com"):
                next_level = next_level[1:]
                continue

            if url in traversed or url == "":
                next_level = next_level[1:]
                continue
            
            print(url)        
            
            if url != next_level[0]:
                traversed = np.append(traversed, next_level[0])
                print("Original url - ",next_level[0])

            next_list = spider(url, traversed, c)
            traversed = np.append(traversed, url)
            next_level = np.append(next_level, next_list)
            next_level = np.unique(next_level)
            gc.collect()
            print("Traversed: ", len(traversed))
            print("Next Level: ", len(next_level))
            print("Last Traverse: ", traversed[-1])
            print("Last Next Level: ", next_level[-1])
            # with open(f"prod_url_list_next_list {time.time()}.txt", "w") as f:
            #     for i in next_level:
            #         f.write(i + "\n")
            print("--------------------------------------------------")
        except:
            print("URL: ", next_level[0])
            print("Connection refused by the server..Retrying")
            return traversed, next_level
    return traversed, next_level

if __name__ == "__main__":
    traversed = np.array([], dtype = object)
    next_level = np.array([], dtype = object)

    with open("prod_url_list_traversed.txt", "r") as f:
        for i in f.readlines():
            traversed = np.append(traversed, i.strip())
    
    with open("prod_url_list_next_list.txt", "r") as f:
        for i in f.readlines():
            next_level = np.append(next_level, i.strip())
    
    host = "127.0.0.1"
    user = "keshav"
    password = "123456"
    database = "chewy"

    mydb = connector.connect(
        host = host,
        user = user,
        password = password,
        database = database
    )

    c = mydb.cursor()
 
    x, y = main(traversed, next_level, c)
    
    c.close()

    with open("prod_url_list_traversed.txt", "w") as f:
        for i in x:
            f.write(i + "\n")

    with open("prod_url_list_next_list.txt", "w") as f:
        for i in y:
            f.write(i + "\n")