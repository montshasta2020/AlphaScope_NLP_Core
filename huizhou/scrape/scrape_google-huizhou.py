
# coding: utf-8

import pandas as pd
from selenium import webdriver 
from bs4 import BeautifulSoup
import time

from datetime import date, timedelta, datetime
import os.path

t0 =  date.today()

#news_url = 'https://www.google.com/search?hl=en&gl=us&tbm=nws&authuser=0&q=徽文化'
news_url="https://www.google.com/#q=%E5%BE%BD%E6%96%87%E5%8C%96&tbm=nws&num=100"
datetime_str = t0
fname1 = 'google-huizhou-news' + '.csv'


def get_columns():
    return ('dt', 'source', 'domain', 'url', 'title', 'summary', 'image', 'brief', 'body', 'raw_page', 'from') 
def get_empty_columns():
    return ('', '', '', '', '', '', '', '', '', '', '') 
def get_empty_columns1():
    return ('', '', '', '', '', '', '', '', '', '', '','') 

def get_data():
    browser = webdriver.Firefox() 
    #browser = webdriver.Chrome('/Users/nhu2000/Downloads/Chromedriver')

    if os.path.isfile(fname1): 
        df = pd.read_csv(fname1)
        idx = len(df.index)
    else:
        df = pd.DataFrame(columns = get_columns())
        idx = 0

    browser.get(news_url)
    time.sleep(5)

    df.head()

    soup = BeautifulSoup(browser.page_source)
    sub_texts = soup.findAll('div', {'class':'g _cy'})

    #print len(sub_texts)
    for txt in sub_texts:

        #set title and url    
        link = txt.find('div', {'class': '_cnc'})

        #check if it is already existed
        t0 = abs(sum(df['url'].str.find(str(link.a['href'])))) 

        #if(tmp_df = df[df['title'].str.contains(link.a.text)]

        #if((df['title'] == link.a.text).any()):
        #if link.a.text in df['title']:
            #do nothing
            #tmp = 0
            #print 'existed'
        #else:

        if(t0 == len(df)):       
        #if(len(tmp_df) == 0):
            print link.a.text
            df.loc[idx] = get_empty_columns()

            #set title and url    
            df.loc[idx]['url'] = link.a['href']
            df.loc[idx]['title'] = link.a.text

            #set image source
            if txt.a.img:
                df.loc[idx]['image'] = txt.a.img['src'] 

            #split between source and time with '-'
            t1 = link.div.text
            t2 = t1.split('-')


            if "ago" in t2[1]:
                df.loc[idx]['dt'] = t0
            else:                    
                df.loc[idx]['dt'] = pd.to_datetime(t2[1]).to_pydatetime().date()

            df.loc[idx]['source'] = t2[0]

            t3 = link.find('div', {'class': 'st'})
            df.loc[idx]['brief'] = t3.text

            #print txt, t2
            df.loc[idx]['from'] = 'google'

            #load_one_page(df, idx, link.a['href'])
            idx += 1 

    df.to_csv(fname1, encoding='utf-8', index=False)

    if(browser):
        browser.quit()


def repeat_get_data():
    while True:
        get_data()
        print get_data
        time.sleep(10) #24*3600)    
        
        
repeat_get_data()


