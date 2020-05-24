from django.shortcuts import render
from joara.models import TodayBest as joara
from bookpal.models import TodayBest as bookpal
from bookpal.forms import optionForm
from web_novel_analysis.base import pie_graph
from web_novel_analysis.base import wordcloud, get_tags
from web_novel_analysis.base import bar_graph
from web_novel_analysis.base import todays_date
from web_novel_analysis.base import search

def main(request):
	form = optionForm
	#나중에 조아라 말고 플랫폼 전체 1개월 데이터로 워드 클라우드 만들기 
	qs = joara.objects.all() + bookpal.objects.all()
	defalt_wc = wordcloud(qs)
	defalt_pie = pie_graph(qs)
	defalt_bar = bar_graph(qs)
	return render(request, 'integration/integration.html', {'form':form, 'wordcloud': defalt_wc, 'pie_graph':defalt_pie, 'bar_graph':defalt_bar})

def result(request):
	#조아라 데이터 구하기
	qs = joara.objects.all() + bookpal.objects.all()

	'''이런식으로 장르 통합하기)
	bl = qs.filter(genre__icontains='BL')
	romanace = qs.filter(genre__icontains='로맨스')
	pantazy = qs.filter(genre__icontains='판타지')
	'''

	form = optionForm(request.GET)
	if form.data['term'] == '1일':
		date = todays_date()
		qs = qs.filter(date__icontains=date)
		_wc = wordcloud(qs)
		_pie = pie_graph(qs)
		_bar = bar_graph(qs)

	return render(request, 'integration/integration.html', {'wordcloud': _wc, 'pie_graph':_pie,  'bar_graph':_bar, 'platform':form.data['platform'], 'genre':form.data['genre'], 'term':form.data['term']})
