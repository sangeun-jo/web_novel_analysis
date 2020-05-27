from django.shortcuts import render
from .models import WebBest
from .models import FreeBest
from .forms import optionForm
from web_novel_analysis.base import pie_graph
from web_novel_analysis.base import wordcloud, get_tags
from web_novel_analysis.base import bar_graph
from web_novel_analysis.base import get_str_date
from web_novel_analysis.base import search

def main(request):
	form = optionForm
	qs1 = WebBest.objects.all()
	qs2 = FreeBest.objects.all()
	qs = qs1.union(qs2)
	defalt_wc = wordcloud(qs)
	defalt_pie = pie_graph(qs)
	defalt_bar = bar_graph(qs)
	return render(request, 'tocsoda/analysis.html', {'form':form, 'wordcloud': defalt_wc, 'pie_graph':defalt_pie, 'bar_graph':defalt_bar})

def result(request):
	#톡소다 전체 데이터 구하기
	qs =  WebBest.objects.all() + FreeBest.objects.all()
	form = optionForm(request.GET)

	if form.data['term'] == '1일':
		date = todays_date()
		qs = qs.filter(date__icontains=date)
		_wc = wordcloud(qs)
		_pie = pie_graph(qs)
		_bar = bar_graph(qs)
	return render(request, 'tocsoda/analysis.html', {'wordcloud':_wc, 'pie_graph':_pie,  'bar_graph':_bar, 'genre':form.data['genre'], 'term':form.data['term']})