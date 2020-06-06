from django.shortcuts import render
#from .models import TodayBest
#from .forms import optionForm
from web_novel_analysis.base import pie_graph, bar_graph
from web_novel_analysis.base import wordcloud, get_tags
from web_novel_analysis.base import filtering
from web_novel_analysis.base import get_str_date
from web_novel_analysis.base import search
import datetime
from django.views.decorators.csrf import csrf_exempt
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import re


def main(request):
	return render(request, 'comment/analysis.html')

# 전체 댓글 페이지 혹은 댓글 첫 페이지 url을 입력해 주세요.
# 로그인한 작가 회원만 가능하게 하도록 하기
# 사이트에 무리를 주지 않도록 꼭 필요할 때만 사용해주세요. 

def joara_comment(url):
	chrome_options = webdriver.ChromeOptions()
	chrome_options.add_argument('headless')
	driver = webdriver.Chrome('D:/chromedriver.exe', options=chrome_options)
	driver.get(url)
	while True:
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
		html = driver.page_source
		soup = BeautifulSoup(html, 'html.parser')
		MoreBtn = soup.select_one('#commentMoreBtn')
		if MoreBtn:
			driver.find_element_by_xpath('//*[@id="commentMoreBtn"]/a').click()
			time.sleep(0.3)
		else:
			break; 
	html = driver.page_source
	soup = BeautifulSoup(html, 'html.parser')
	comments = soup.find_all('p', class_='comment')
	driver.close()
	commentList = []
	for comment in comments:
		commentList.append(comment.text)
	return commentList

def bookpal_comment(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome('D:/chromedriver.exe', options=chrome_options)

    commentList = []
    cnt = 1
    
    while True:  
        driver.get(url +'?page=' + str(cnt))
        cnt = cnt + 1
        time.sleep(0.3)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        comments = soup.find_all('div', class_='con-comm')
        if comments:
            for comment in comments:
                commentList.append(comment.text.strip())
        else:
            break; 
    driver.close()
    return commentList

def tocsoda_comment(url):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome('D:/chromedriver.exe', options=chrome_options)
    cnt = 1
    commentList = []
    urlList = url.split('?')
    while True:
        newUrl = urlList[0].replace('productView', '')+'selectEpisodeCommentList?' + urlList[1]+ '&page=' + str(cnt)
        driver.get(newUrl)
        time.sleep(0.3)
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        comments = re.findall(r'\"cmntCntts\":\"(.*?)\"' , soup.pre.text)
        if comments == []:
            break
        else:
            for comment in comments:
                print(comment)
                commentList.append(comment)     
        cnt = cnt+1
    driver.close()
    return commentList

@csrf_exempt
def result(request):
	return render(request, 'comment/analysis.html')

@csrf_exempt
def search(request):
	url = request.POST.get('comment_url', '')
	if 'joara' in url:
		comment = joara_comment(url)
	if 'bookpal' in url:
		comment = bookpal_comment(url)
	if 'tocsoda' in url:
		comment = tocsoda_comment(url)
	w_keyword = get_tags(comment)
	b_keyword = get_tags(comment, 20)
	return render(request, 'comment/analysis.html', {'wordcloud':wordcloud(w_keyword), 'bar_graph':bar_graph(b_keyword)})