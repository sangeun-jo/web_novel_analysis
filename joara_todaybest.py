from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
import re
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_novel_analysis.settings")
import django
django.setup()
from joara.models import TodayBest

now = time.localtime()

hangul = re.compile('[^ ㄱ-ㅣ가-힣]+') 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('headless')
driver = webdriver.Chrome('D:/chromedriver.exe', options=chrome_options)

driver.get('http://www.joara.com/best/today_best_list.html?page_no=1&sl_subcategory=all')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')

book_list = soup.find_all('td', class_='book_data_intro_form subject_long')

date = str(now.tm_year)+str(now.tm_mon).zfill(2)+str(now.tm_mday).zfill(2)

for book in book_list:
    try:
        genre = book.strong.text
        title = book.a.text.replace(genre, '').strip()
        intro = book.span.text
    except:
        genre = 'failed'
        title = ''
        intro = book
    TodayBest(date=date, genre=genre, title=title, intro=intro).save()
driver.close()