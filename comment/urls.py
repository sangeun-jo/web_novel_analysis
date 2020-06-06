from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main, name='comment'),
	url(r'^analysis$', views.search, name='analysis'),
]