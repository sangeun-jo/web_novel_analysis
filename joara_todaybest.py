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

book_list = soup.select('#content > table > tbody > tr > td.book_data_intro_form.subject_long')

for book in book_list:
	#나중에 데이터 처리 시 활용
	#genre = hangul.sub('', str(re.search(r'\[(.*?)\]' , "장르").group())) []없애기 
	#title = hangul.sub(' ', str(re.search(r'\](.*?)\<' , "제목"))).strip() 제목 예쁘게 추출
	try: 
		genre = book.strong.text
		title = book.a.text.replace(genre, '').strip()
		intro = book.span.text
	except:
		genre = '실패'
		title = ''
		intro = book
	TodayBest(year=now.tm_year, month=now.tm_mon, day=now.tm_mday, genre=genre, title=title, intro=intro).save()
driver.close()