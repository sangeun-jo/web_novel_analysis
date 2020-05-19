from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main, name='keyword_main'), #localhost:8000
	url(r'^test/$', views.test, name='test'), #localhost:8000/test/
	url(r'^search/$', views.search, name='search'), #localhost:8000/search/
]

