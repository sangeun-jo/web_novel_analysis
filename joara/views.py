from django.shortcuts import render
from .models import TodayBest
import pandas as pd
from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter
import re
import matplotlib.pyplot as plt
import io
import urllib, base64


def keyword(request):
	return(request, 'keyword_analysis/keyword.html')

def get_tags(text, ntags=100): #상위 100개만 추출(나중에 사용자한테 입력받게 하는 것도 고려)
    spliter = Twitter()
    nouns = spliter.nouns(text)
    nouns = [n for n in nouns if len(n) > 1] #한글자 단어 삭제 
    count = Counter(nouns)
    return_list = {}
    for n, c in count.most_common(ntags):
        if n == '표지' or n == '소설':
            continue
        return_list[n] = c
    return return_list

def wordcloud():
	wc = WordCloud(font_path='C:/Windows/Fonts/batang.ttc', 
            background_color='white', 
            width=900, 
            height=300, 
            max_words=100, 
            max_font_size=200)
	txt = ''

	for nov in TodayBest.objects.all():
		txt = txt + ' ' + nov.title + ' ' + nov.intro
		kor_eng = re.compile('[^ a-zA-Zㄱ-ㅣ가-힣]+') #한글, 영어만 추출 
	cleaned_text = kor_eng.sub(' ', txt)
	keyword = get_tags(cleaned_text)
	wc_img = wc.generate_from_frequencies(keyword)
	wc_img.to_file('D:/ProjectFiles/gradualation/Django/web_novel_analysis/joara/static/wordcloud.png')
	'''
	plt.imshow(wc_img, interpolation='bilinear')
	plt.axis("off")
	image = io.BytesIO()
	plt.savefig(image, format='png')
	image.seek(0)  # rewind the data
	string = base64.b64encode(image.read())
	image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
	return image_64
'''
def pie_graph():
	from matplotlib import font_manager, rc
	font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
	rc('font', family=font_name)
	genre = []
	for nov in TodayBest.objects.all():
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
	plt.pie(group_size, 
        labels=group_name, 
        autopct='%1.2f%%', # second decimal place
        shadow=True, 
        startangle=90,
        textprops={'fontsize': 9}) # text font size

	plt.axis('equal') #  equal length of X and Y axis
	#plt.title('인기 장르', fontsize=20)
	fig = plt.gcf() 
	fig.set_size_inches(4.2, 3.0)
	fig.savefig('D:/ProjectFiles/gradualation/Django/web_novel_analysis/joara/static/pie_graph.png') 
	'''
	plt.axis("off")
	image = io.BytesIO()
	plt.savefig(image, format='png')
	image.seek(0)  # rewind the data
	string = base64.b64encode(image.read())
	image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
	return image_64
'''

def main(request):
	#단순히 디비 보여주는 코드 
	#realtimebests = RealtimeBest.objects.all()
	#context = {'realtimebests':realtimebests}
	#return render(request, 'joara/analysis.html', context)
	pie_graph()
	wordcloud()
	return render(request, 'joara/analysis.html')




