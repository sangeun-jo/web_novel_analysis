from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main, name='bookpal'), #localhost:8000
	url(r'^analysis/$', views.result, name='analysis'),
	url(r'^search/$', views.search, name='search'), #localhost:8000/search/
]