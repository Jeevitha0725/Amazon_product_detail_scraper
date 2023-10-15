import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

def get_title(soup):
    try:
        title=soup.find("span", attrs={"id":"productTitle"}).text.strip()
    except AttributeError:
        title=""
    return title

def get_price(soup):
    try:
        price=soup.find("span",attrs={"class":"a-offscreen"}).string.strip()
    except AttributeError:
        price=""
    return price

if __name__=="__main__":
    import requests
    from bs4 import BeautifulSoup


    Headers=({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36","Accept-Language": "en-US, en;q=0.5"})
    r=requests.get("https://www.amazon.com/s?k=iphone+14+pro+max+phone+case&sprefix=iphone%2Caps%2C1477&ref=nb_sb_ss_ts-doa-p_1_6", headers=Headers)
    print(r)
    Soup=BeautifulSoup(r.content,"html.parser")
    links=Soup.find_all("a",attrs={"class":"a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"})

    Link=[]
    for i in links:
        Link.append(i.get("href"))

    Product_details={"Title":[], "Price":[]}

    for j in Link:
        Product_page=requests.get("https://www.amazon.com"+j,headers=Headers)
        soup=BeautifulSoup(Product_page.content,"html.parser")
        Product_details["Title"].append(get_title(soup))
        Product_details["Price"].append(get_price(soup))

    dataframe = pd.DataFrame.from_dict(Product_details)
    dataframe["Title"].replace("", np.nan, inplace=True)
    DF = dataframe.dropna(subset="Title")
    DF.to_csv(r"C:\Users\sjeev\Documents\Python\Web_scraping\Amazon_phone_case.csv", header=True, index=False)

print(DF)