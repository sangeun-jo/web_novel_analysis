from django.shortcuts import render
from joara.models import TodayBest

def main(request):
	return render(request, 'keyword_analysis/keyword.html')

def test(request):
	return render(request, 'keyword_analysis/test.html')

def search(request):
	qs = TodayBest.objects.all()
	q = request.GET.get('q', '')
	if q:
		qs = qs.filter(title__icontains=q)
	return render(request, 'keyword_analysis/keyword.html', {'search_result':qs})