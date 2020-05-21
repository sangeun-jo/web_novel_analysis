from django.shortcuts import render
from joara.models import TodayBest
import re
from konlpy.tag import Twitter
from collections import Counter
import urllib, base64
import matplotlib.pyplot as plt
import io

def search(request):
	#애도 전체 데이터로 구현하기
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
	kor_eng = re.compile('[^ a-zA-Zㄱ-ㅣ가-힣]+') #한글, 영어만 추출 
	wc = WordCloud(font_path='C:/Windows/Fonts/mb.ttf', 
            background_color='white', 
            width=900, 
            height=360, 
            max_words=100, 
            max_font_size=200)
	txt = ''
	for nov in qs:
		txt = txt + ' ' + nov.title + ' ' + nov.intro
	cleaned_text = kor_eng.sub(' ', txt)
	keyword = get_tags(cleaned_text)
	wc_img = wc.generate_from_frequencies(keyword)
	plt.figure(figsize=(20, 6))
	plt.imshow(wc_img, interpolation='bilinear')
	plt.axis("off")
	image = io.BytesIO()
	plt.savefig(image, format='png', bbox_inches='tight', pad_inches=0.1)
	image.seek(0)  
	string = base64.b64encode(image.read())
	image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
	return image_64