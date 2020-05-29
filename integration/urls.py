from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main), #localhost:8000
	url(r'^search/$', views.search, name='search'), #localhost:8000/search/
	url(r'^analysis/', views.result, name='analysis'), #localhost:8000/form_test/
]

