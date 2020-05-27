from django.shortcuts import render
from joara.models import TodayBest
from .forms import optionForm
from web_novel_analysis.base import pie_graph
from web_novel_analysis.base import wordcloud, get_tags
from web_novel_analysis.base import bar_graph
from web_novel_analysis.base import get_str_date
from web_novel_analysis.base import search
import datetime
from django.views.decorators.csrf import csrf_exempt


def main(request):
	form = optionForm
	#qs = TodayBest.objects.all()
	#defalt_wc = wordcloud(qs)
	#defalt_pie = pie_graph(qs)
	#defalt_bar = bar_graph(qs)
	#return render(request, 'joara/analysis.html', {'form':form, 'wordcloud': defalt_wc, 'pie_graph':defalt_pie, 'bar_graph':defalt_bar})
	return render(request, 'joara/analysis.html', {'form':form })


def filtering(request, qs):
	# 빈 쿼리셋 만들기
	genredata = TodayBest.objects.none()
	termdata = TodayBest.objects.none()
	#form = optionForm(request.POST)

	# 장르 필터링(함수화)
	genres = request.POST.getlist('genre') # 체크박스에 선택된 장르 가져오기
	for gen in genres:
		gen = '['+gen+']'
		genredata = genredata.union(qs.filter(genre__iexact=gen))


	# 1일, 1주일, 한달 간격 데이터 반환 시 사용.
	for day in range(0, int(request.POST['term'])): 
	#for day in range(0, int(form.data['term'])): 
		d = datetime.timedelta(days = day)
		_d = datetime.datetime.now() - d
		year = str(_d.year)
		mon = str(_d.month).zfill(2)
		day = str(_d.day).zfill(2)
		date = year+mon+day
		termdata = termdata.union(qs.filter(date__iexact=date))

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
	return genredata.intersection(termdata)

@csrf_exempt
def result(request):
	qs = TodayBest.objects.all()
	filtered = filtering(request, qs)
	# 객체 반환
	return render(request, 'joara/analysis.html', {
		'wordcloud':wordcloud(filtered), 
		'pie_graph':pie_graph(filtered),  
		'bar_graph':bar_graph(filtered), 
		#'genre':form.data['genre'], 
		#'term':form.data['term'],
	})
	