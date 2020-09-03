import time
from selenium import webdriver
from bs4 import BeautifulSoup, NavigableString, Tag
import requests
import pandas as pd
import logging
import csv
import argparse



logging.basicConfig(level=logging.CRITICAL)

parser = argparse.ArgumentParser(description='fill arguement')

parser.add_argument('--novel_name', type=str, required=False,
                    help='input the novel name')


parser.add_argument('--page', type=int, required=False, default=1000,
                    help='input the novel name')

parser.add_argument('--experiment', type=str, required=True,
                    help = 'input the execution experiment name')


parser.add_argument('--url', type=str, required=False, default="https://www.ptwxz.com/",
                    help= "input novel table of content's url")

args = parser.parse_args()

logging.debug("novel name", args.novel_name)
logging.debug("novel page", args.page)

count_page = args.page



browser = webdriver.Chrome()
url=args.url
browser.get(url)


soup = BeautifulSoup(browser.page_source, 'html.parser')

data = pd.DataFrame()


#count the page
count = 0
for i in soup.find_all('li'):
    for j in i.find_all('a', href=True):
    
        if(count > count_page):
            break
        
        newurl = url+'/'+j.get('href')
        response = requests.get(newurl, verify=False, headers={
            "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"
        })
        print("new url", newurl)
        logging.debug("status code ", response.status_code)
        logging.debug("web encode ",response.encoding)
        logging.debug("apparent encode", response.apparent_encoding)
        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, 'html.parser')


        title = soup.find("title")
        
        text = ""

        for i in soup.find_all('br'):
            next_s = i.nextSibling
            if(next_s and type(next_s) == "<class 'bs4.element.NavigableString'>"):
                continue
            if(isinstance(next_s, Tag)):
                continue
            #print(next_s)
            text += str(next_s)
        if(title.string != "404 Not Found"):    
            series = pd.DataFrame({
                "title": title.string,
                "desc" : text
            }, index=[str(count)])
            data = data.append(series)
            count += 1
        else:
            print("error 404")


data_csv = data.to_csv(args.experiment+'.csv')
print(data_csv)
