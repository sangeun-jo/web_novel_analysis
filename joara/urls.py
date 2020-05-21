from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main, name='joara'), 
	url(r'^keyword/$', views.keyword, name='keyword'), 
]