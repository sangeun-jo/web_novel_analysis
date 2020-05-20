from django.shortcuts import render
from joara.models import TodayBest
from .forms import UserForm
from .forms import optionForm
import time
from wordcloud import WordCloud
import re
from konlpy.tag import Twitter
from collections import Counter
import urllib, base64
import matplotlib.pyplot as plt
import io

def main(request):
	form = optionForm
	return render(request, 'keyword_analysis/keyword.html', {'form':form})

def search(request):
	qs = TodayBest.objects.all()
	q = request.POST.get('q', '')
	if q:
		qs = qs.filter(title__icontains=q)
	return render(request, 'keyword_analysis/keyword.html', {'search_result':qs})

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

def wordcloud(qs):
	wc = WordCloud(font_path='C:/Windows/Fonts/batang.ttc', 
            background_color='white', 
            width=900, 
            height=300, 
            max_words=100, 
            max_font_size=200)
	txt = ''

	for nov in qs:
		txt = txt + ' ' + nov.title + ' ' + nov.intro
		kor_eng = re.compile('[^ a-zA-Zㄱ-ㅣ가-힣]+') #한글, 영어만 추출 
	cleaned_text = kor_eng.sub(' ', txt)
	keyword = get_tags(cleaned_text)
	wc_img = wc.generate_from_frequencies(keyword)
	wc_img.to_file('D:/ProjectFiles/gradualation/Django/web_novel_analysis/keyword_analysis/static/wordcloud.png')

def options_form(request):
	now = time.localtime()
	qs = TodayBest.objects.all()
	form = optionForm(request.GET)
	if form.data['term'] == 'day':
		year = str(now.tm_year)
		month = str(now.tm_mon)
		day = str(now.tm_mday)
		date = year+month+day
		qs = qs.filter(date__icontains=date)
		wordcloud(qs)
	return render(request, 'keyword_analysis/keyword.html')
