from django.shortcuts import render
from .models import TodayBest
from .forms import optionForm
from web_novel_analysis.base import pie_graph, bar_graph
from web_novel_analysis.base import wordcloud, get_tags
from web_novel_analysis.base import filtering
from web_novel_analysis.base import get_str_date
from web_novel_analysis.base import search
import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse


def main(request):
	form = optionForm
	#qs = TodayBest.objects.all()
	#defalt_wc = wordcloud(qs)
	#defalt_pie = pie_graph(qs)
	#defalt_bar = bar_graph(qs)
	#return render(request, 'joara/analysis.html', {'form':form, 'wordcloud': defalt_wc, 'pie_graph':defalt_pie, 'bar_graph':defalt_bar})
	return render(request, 'joara/analysis.html', {'form':form })

@csrf_exempt
def result(request):
    form = optionForm
    filtered = filtering(request, 'joara-tobe.csv')
    if filtered.empty:
        return render(request, 'joara/analysis.html', {'none':'검색결과가 없습니다.'})
    w_keyword = get_tags(filtered)
    b_keyword = get_tags(filtered, 20)
    return render(request, 'joara/analysis.html', {
    'wordcloud':wordcloud(w_keyword), 
    'pie_graph':pie_graph(filtered),  
    'bar_graph':bar_graph(b_keyword), 
    'form':form, 
    })

@csrf_exempt
def results(request):
    form = optionForm
    filtered = filtering(request, 'joara-tobe.csv')
    if filtered.empty:
        return render(request, 'joara/results.html', {'none':'검색결과가 없습니다.'})
    w_keyword = get_tags(filtered)
    top_ten = get_tags(filtered, 10)
    top_keys = top_ten.keys()
    top_items = top_ten.items()
    return render(request, 'joara/results.html', {
        'form':form,
        'wordcloud':wordcloud(w_keyword), 
        'top_keys':top_keys, 
        'top_items':top_items}) 