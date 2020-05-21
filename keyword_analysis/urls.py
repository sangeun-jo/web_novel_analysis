from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.main, name='keyword_main'), #localhost:8000
	url(r'^search/$', views.search, name='search'), #localhost:8000/search/
	url(r'^form_test/$', views.result, name='form'), #localhost:8000/form_test/
]

