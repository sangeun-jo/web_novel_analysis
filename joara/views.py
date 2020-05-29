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
	qs = TodayBest.objects.all()
	filtered = filtering(request, qs)
	return render(request, 'joara/analysis.html', {
	'wordcloud':wordcloud(filtered), 
	'pie_graph':pie_graph(filtered),  
	'bar_graph':bar_graph(filtered), 
	})

	