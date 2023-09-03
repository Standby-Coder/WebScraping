import requests
import bs4

def get_title(soup): 
    try:
        title = soup.find("h1", attrs = {"data-testid" : "product-title-heading"}).get_text()
    except:
        title = ""
    return title

def get_brand(soup):
    try:
        brand = soup.find("span", attrs = {"data-testid" : "manufacture-name"})
        brand = brand.find("a").get_text()
    except:
        brand = ""
    return brand

def get_advertised_price(soup):
    try:
        price = soup.find("div", attrs={"data-testid": "advertised-price"}).next_element.strip()
    except:
        price = ""
    return price

def get_autoship_price(soup):
    try:
        price = soup.find("div", attrs={"data-testid": "autoship-price"}).next_element.strip()
    except:
        price = ""
    return price

def get_spec(soup):
    spec_info = {}
    try:
        info = soup.find("div", attrs={"data-event-label" : "product-detail-description"})
        spec = info.find(lambda tag:tag.name == "section" and "Specifications" in tag.text)
        spec_info["weight"] = get_weight(spec)
        spec_info["item_number"] = get_item_number(spec)

        if(check_prescription(soup)):
            spec_info["Prescription"] = "Rx"
            spec_info["desc"] = get_desc_rx(soup)
        else:
            spec_info["Prescription"] = "Non-Rx"
            spec_info["desc"] = get_desc(spec)

    except:
        spec_info["weight"] = ""
        spec_info["item_number"] = ""
        spec_info["Prescription"] = ""
        spec_info["desc"] = ""

    return spec_info

def get_weight(soup):
    try:
        table = soup.find("table")
        weight = table.find("th", text = "Weight").next_sibling.get_text()
    except:
        weight = ""

    return weight

def get_desc(soup):
    try:
        sect = soup.find_previous_sibling().next_element
        desc = sect.text
    except:
        desc = ""
    
    return desc

def get_item_number(soup):
    try:
        table = soup.find("table")
        item_number = table.find("th", text = "Item Number").next_sibling.get_text()
    except:
        item_number = ""
    return item_number

def get_desc_rx(soup):
    try:
        info = soup.find("div", attrs={"data-event-label" : "product-detail-description"})
        head = info.find(lambda tag:tag.name == "h3" and "Details" in tag.text)
        div = head.find_next("div")
        desc = div.find("p").get_text()
    except:
        desc = ""

    return desc

def check_prescription(soup):
    try:
        man = soup.find("span", attrs = {"data-testid" : "manufacture-name"})
        div = man.find_next_sibling("div")
        if "Prescription" in div.get_text():
            return True
        else:
            return False
    except:
        return False
    
