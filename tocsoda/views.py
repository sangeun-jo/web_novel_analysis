from django.shortcuts import render
from .models import WebBest, FreeBest
from .forms import optionForm
from web_novel_analysis.base import pie_graph, bar_graph
from web_novel_analysis.base import wordcloud, get_tags
from web_novel_analysis.base import filtering
from web_novel_analysis.base import get_str_date
from web_novel_analysis.base import search
import datetime
from django.views.decorators.csrf import csrf_exempt


def main(request):
	form = optionForm
	return render(request, 'tocsoda/analysis.html', {'form':form })

@csrf_exempt
def result(request):
	web = filtering(request, WebBest.objects.all())
	free = filtering(request, FreeBest.objects.all())
	filtered = web.union(free)
	if not filtered:	
		return render(request, 'tocsoda/analysis.html', {'none':'검색결과가 없습니다.'})
	w_keyword = get_tags(filtered)
	b_keyword = get_tags(filtered, 20)

	# 객체 반환
	return render(request, 'tocsoda/analysis.html', {
		'wordcloud':wordcloud(w_keyword), 
		'pie_graph':pie_graph(filtered),  
		'bar_graph':bar_graph(b_keyword), 
		#'genre':form.data['genre'], 
		#'term':form.data['term'],
	})
	