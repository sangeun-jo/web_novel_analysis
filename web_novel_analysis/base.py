from django.shortcuts import render
from joara.models import TodayBest as joara
from bookpal.models import TodayBest as bookpal
import re, io
from konlpy.tag import Twitter
from collections import Counter
import urllib, base64
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import requests
import time, datetime
from wordcloud import WordCloud


#======== 검색 모듈 ========== 

def search(request):
	url = request.POST.get('comment_url', '')
	return render(request, 'comment/analysis.html', {'comment_url':url})

#==========키워드 분석 모듈 ===========

#쿼리셋 주면 데이터 전처리해서 단어 개수 세어줌 
def get_tags(data, ntags=50): #상위 100개만 추출(나중에 사용자한테 입력받게 하는 것도 고려)
	hangul = re.compile('[^ a-zA-Z0-9ㄱ-ㅣ가-힣]+') 

	txt = ''

	if type(data) == list:
		for nov in data:
			txt = txt + ' ' + nov
	else: 
		for nov in data:
			txt = txt + ' ' + nov.title + ' ' + nov.intro

	cleaned_text = hangul.sub(' ', txt)
	spliter = Twitter()
	nouns = spliter.nouns(cleaned_text)
	nouns = [n for n in nouns if len(n) > 1] #한글자 단어 삭제 
	count = Counter(nouns)
	return_dict = {}

	#return_dict = {n, c in cont.most_common(ntags) if n not in ['표지', '소설', '그녀', '무료', '연재']}
	for n, c in count.most_common(ntags):
		#if n == '표지' or n == '소설':
		if n not in ['표지', '소설', '여주', '그녀', '사람', '연재', '무료', '신작']:
			return_dict[n] = c
	return return_dict

def wordcloud(keyword):
	wc = WordCloud(font_path='C:/Windows/Fonts/malgun.ttf', 
            background_color='white', 
            width=900, 
            height=360, 
            max_words=100, 
            max_font_size=200, 
    	)

	try:
		wc_img = wc.generate_from_frequencies(keyword)
	except:
		return 'null'
	plt.figure(figsize=(12, 5))
	plt.imshow(wc_img, interpolation='bilinear')
	plt.axis("off")
	image = io.BytesIO()
	plt.savefig(image, format='png', bbox_inches='tight', pad_inches=0.1)
	image.seek(0)  
	string = base64.b64encode(image.read())
	image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
	return image_64

def bar_graph(keyword):
	font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
	rc('font', family=font_name, size=8)
	plt.figure(figsize=(7, 3.9))
	#keyword = get_tags(qs, 20)
	values = []
	keys = [] 
	for key in keyword.keys():
		keys.append(key)
		values.append(keyword[key])
	plt.bar(range(len(values)), values)
	#plt.xlabel('인기 키워드')
	#plt.ylabel('빈도수')
	plt.xticks(range(len(keys)),keys, rotation=40)
	plt.bar(range(len(values)), values)
	image = io.BytesIO()
	plt.savefig(image, format='png', bbox_inches='tight', pad_inches=0.1)
	image.seek(0)  
	string = base64.b64encode(image.read())
	image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
	return image_64



#=======장르 분석 모듈 ==========

def pie_graph(qs):
	font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
	rc('font', family=font_name)
	genre = []
	rat = []
	for nov in qs:
		nov.genre
		genre.append(nov.genre)
		rat = Counter(genre)
	group_name = []
	group_size = []
	for genre in rat:
		group_size.append(rat[genre])
		genre = genre.replace('[', '')
		genre = genre.replace(']', '')
		group_name.append(genre)
	plt.figure(figsize=(4, 3.6))
	plt.pie(group_size, 
		labels=group_name, 
		autopct='%1.2f%%', # second decimal place
		shadow=True, 
		textprops={'fontsize': 8}) # text font size
	plt.axis('equal') #  equal length of X and Y axis
	#plt.title('인기 장르', fontsize=20)
	plt.axis("off")
	image = io.BytesIO()
	plt.savefig(image, format='png')
	image.seek(0)  # rewind the data
	string = base64.b64encode(image.read())
	image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
	return image_64


#======= 필터링 모듈 =========

def filtering(request, qs):
	# 빈 쿼리셋 만들기
	genredata = qs.none()
	termdata = qs.none()
	#form = optionForm(request.POST)

	# 장르 필터링


	genres = request.POST.getlist('genre') # 체크박스에 선택된 장르 가져오기

	for gen in genres:
		gen = '['+gen+']'
		try:
			genredata = genredata.union(qs.filter(genre__iexact=gen))
		except:
			continue
	#print('장르', genredata)
	# 1일, 1주일, 한달 간격 데이터 반환 시 사용.
	
	term = int(request.POST['term'])

	for day in range(0, term): 
		d = datetime.timedelta(days = day)
		_d = datetime.datetime.now() - d
		year = str(_d.year)
		mon = str(_d.month).zfill(2)
		day = str(_d.day).zfill(2)
		date = year+mon+day
		try:
			termdata = termdata.union(qs.filter(date__iexact=date))
		except:
			continue

	'''
	# 시작날짜, 끝날짜 주면 그 사이에 있는 데이터 반환함. 캘린더로 입력 받을 시 사용
	d = datetime.timedelta(days = int(request.POST['term'])) # n 일전 날짜 구하기 
	_d = datetime.datetime.now() - d 
	year = str(_d.year)
	mon = str(_d.month).zfill(2)
	day = str(_d.day).zfill(2)
	start_date = year+mon+day
	termdata = qs.filter(date__range=[start_date, get_str_date()])
	'''	

	# 여기서 문제임 
	return termdata.intersection(genredata)


# ========= 기타 유용한 모듈들 =========

def get_str_date(date = time.localtime()):
	year = str(date.tm_year)
	month = str(date.tm_mon).zfill(2)
	day = str(date.tm_mday).zfill(2)
	str_date = year+month+day
	return str_date 