from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main, name='relation'), #localhost:8000
	url(r'^analysis$', views.result, name='analysis'),
]