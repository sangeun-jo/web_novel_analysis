#!/usr/bin/env python
# coding: utf-8

# In[136]:


from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
import re
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_novel_analysis.settings")
#os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
import django
django.setup()
from bookpal.models import TodayBest

now = time.localtime()
date = str(now.tm_year)+str(now.tm_mon)+str(now.tm_mday)
hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
driver = webdriver.Chrome('D:/chromedriver.exe', options=chrome_options)

driver.get('https://novel.bookpal.co.kr/novel@best?depth=list_search')
time.sleep(10)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

titles = soup.select_one('#list_items').find_all('div', class_='title') #제목 리스트 
gks = soup.find_all('p', class_='info m-t-m clear-f') #키워드, 장르 리스트 
introes = soup.find_all('p', class_='summary') #소개글 리스트

for tit, gk, intr in zip(titles, gks, introes):
   
    title = tit.text.strip()
    genre = re.search(r'\[(.*?)\]', gk.text).group() 
    intro = gk.text.replace(genre, '') + ' ' + intr.text
    TodayBest(date=date, genre=genre, title=title, intro=intro).save()
driver.close()


# In[ ]:




