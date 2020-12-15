#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
import re
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_novel_analysis.settings")
#os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django
django.setup()
from tocsoda.models import WebBest, FreeBest
import re

now = time.localtime()
date = str(now.tm_year)+str(now.tm_mon).zfill(2)+str(now.tm_mday).zfill(2)
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
driver = webdriver.Chrome('/home/ubuntu/Downloads/chromedriver', options=chrome_options)
def crawler(kind):
    driver.get('http://www.tocsoda.co.kr/totalBestView/' + kind) #00023
    if kind == '00023': #웹소설 
        driver.find_element_by_xpath('//*[@id="TOTAL_ORDERBY"]/li[3]/span/label').click()
    elif kind == '00024': #자유연재 
        driver.find_element_by_xpath('//*[@id="TOTAL_ORDERBY"]/li[1]/span/label').click()
    
    time.sleep(10)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.select_one('#TOTAL_PRODUCT_LIST')
    
    titles = data.find_all('span', class_='txt')
    genres = data.find_all('span', class_='total')
    introes = data.find_all('p', class_='desc')

    for title, genre,intro  in zip(titles, genres, introes):
        title = title.text.strip()
        genre = re.search(r'\[(.*?)\]', genre.text).group() 
        intro = intro.text
        if kind == '00023':
            WebBest(date=date, genre=genre, title=title, intro=intro).save()
        elif kind == '00024':
            FreeBest(date=date, genre=genre, title=title, intro=intro).save()
crawler('00023') #웹소설
crawler('00024') #자유연재
driver.close()

