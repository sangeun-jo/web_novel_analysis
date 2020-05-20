from django.shortcuts import render
from joara.models import TodayBest
from .forms import UserForm
from .forms import optionForm
import time

def main(request):
	form = optionForm
	return render(request, 'keyword_analysis/keyword.html', {'form':form})

#def test(request):
#	return render(request, 'keyword_analysis/test.html')

def search(request):
	qs = TodayBest.objects.all()
	q = request.POST.get('q', '')
	if q:
		qs = qs.filter(title__icontains=q)
	return render(request, 'keyword_analysis/keyword.html', {'search_result':qs})

'''
def form_test(request):
	form = UserForm(request.GET)
	print(form)
	return render(request, 'keyword_analysis/keyword.html', {'form_result':form})
'''

def options_form(request):
	now = time.localtime()
	qs = TodayBest.objects.all()
	form = optionForm(request.GET)
	if form.data['term'] == 'day':
		year = str(now.tm_year)
		month = str(now.tm_mon)
		day = str(now.tm_mday)
		date = year+month+day
		print(date)
		qs = qs.filter(date__icontains=date)
		print(qs)
	return render(request, 'keyword_analysis/keyword.html', {'day_result':qs})
