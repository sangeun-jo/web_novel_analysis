from django.shortcuts import render
import re, io
from konlpy.tag import Twitter
from collections import Counter
import urllib, base64
import matplotlib.pyplot as plt
from matplotlib import font_manager, rc
import requests
import time, datetime
from wordcloud import WordCloud
import os
import boto3
import pandas as pd
from io import StringIO
from pytz import timezone
import random

#======== s3 모듈 ===========

def read_data_from_s3(db_name):
    
    f = open("/home/ubuntu/Downloads/rootkey.txt", 'r')
    rootkey = f.read().splitlines()
    f.close()
    
    aws_id = rootkey[0]
    aws_secret = rootkey[1]
    
    bucket_name = 'web-novel-db'
    object_key = db_name
    client = boto3.client('s3',aws_access_key_id= aws_id, aws_secret_access_key=aws_secret)
    csv_obj = client.get_object(Bucket=bucket_name, Key=object_key)
    body = csv_obj['Body']
    csv_string = body.read().decode('utf-8')
    return pd.read_csv(StringIO(csv_string))

#======== 검색 모듈 ========== 

def search(request):
	url = request.POST.get('comment_url', '')
	return render(request, 'comment/analysis.html', {'comment_url':url})

#==========키워드 분석 모듈 ===========

#데이터 전처리
def get_tags(data, ntags=50): #상위 50개만 추출
    hangul = re.compile('[^ a-zA-Z0-9ㄱ-ㅣ가-힣]+') 

    txt = ''

    data = data.title.values.tolist() + data.intro.tolist()
    
    for nov in data:
        if type(nov) != str:
                continue
        txt = txt + ' ' + nov
    
    cleaned_text = hangul.sub(' ', txt)
    spliter = Twitter()
    nouns = spliter.nouns(cleaned_text)
    nouns = [n for n in nouns if len(n) > 1] #한글자 단어 삭제 
    count = Counter(nouns)
    return_dict = {}
    
    for n, c in count.most_common(ntags):
        if n not in ['표지', '소설', '여주', '그녀', '사람', '연재', '무료', '신작']:
            return_dict[n] = c
    return return_dict

def wordcloud(keyword):
    random.random()
    r = random.randrange(1,4) 

    season = ['spring', 'summer', 'copper', 'winter']
    wc = WordCloud(font_path='/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf',  
            background_color='white', 
            colormap = season[r],
            width=1000, 
            height=450, 
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
	try:
		font_name = font_manager.FontProperties(fname="C:/Windows/Fonts/malgun.ttf").get_name()
	except:
		font_name = font_manager.FontProperties(fname="/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf").get_name()
	rc('font', family=font_name, size=8)
	plt.figure(figsize=(7, 3.9))
	#keyword = get_tags(qs, 20)
	values = []
	keys = [] 
	for key in keyword.keys():
		keys.append(key)
		values.append(keyword[key])
	plt.bar(range(len(values)), values)
	plt.xticks(range(len(keys)),keys, rotation=40)
	plt.bar(range(len(values)), values)
	image = io.BytesIO()
	plt.savefig(image, format='png', bbox_inches='tight', pad_inches=0.1)
	image.seek(0)  
	string = base64.b64encode(image.read())
	image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
	return image_64



#=======장르 분석 모듈 ==========

def pie_graph(df):
	try:
		font_name = font_manager.FontProperties(fname="C:/Windows/Fonts/malgun.ttf").get_name()
	except:
		font_name = font_manager.FontProperties(fname="/usr/share/fonts/truetype/nanum/NanumBarunGothic.ttf").get_name()
	rc('font', family=font_name)
	genre = df.genre.values.tolist()
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

def filtering(request, db_name):
    
    df = read_data_from_s3(db_name)
    
    term = int(request.POST['term'])
    genres = request.POST.getlist('genre')
    
    today = datetime.datetime.now(timezone('Asia/Seoul'))
    start = today - datetime.timedelta(days = term-1)
    end_day = int(today.strftime('%Y%m%d')) 
    start_day = int(start.strftime('%Y%m%d')) 
    
    return df[(start_day <= df['date']) & (df['date'] <= end_day) & (df['genre'].isin(genres))]

# 전체 데이터에서 기간별로 불러오기 
def get_weeks_data(term):
    joara = read_data_from_s3('joara-tobe.csv')
    bookpal = read_data_from_s3('bookpal-tobe.csv')
    tocsoda_web = read_data_from_s3('tocsoda-tobe-web.csv')
    tocsoda_free = read_data_from_s3('tocsoda-tobe-free.csv')

    novel = pd.concat([joara,bookpal, tocsoda_web, tocsoda_free])

    today = datetime.datetime.now(timezone('Asia/Seoul'))
    start = today - datetime.timedelta(days = term-1) 
    end_day = int(today.strftime('%Y%m%d')) 
    start_day = int(start.strftime('%Y%m%d')) 
    return novel[(start_day <= novel['date']) & (novel['date'] <= end_day)]


# ========= 기타 유용한 모듈들 =========

def get_str_date(date = time.localtime()):
	year = str(date.tm_year)
	month = str(date.tm_mon).zfill(2)
	day = str(date.tm_mday).zfill(2)
	str_date = year+month+day
	return str_date 