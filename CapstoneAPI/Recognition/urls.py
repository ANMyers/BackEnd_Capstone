from django.conf.urls import url
from Recognition.views import *

app_name = "Recognition"
urlpatterns = [
	url(r'^kmeans/$', kmeans, name='kmeans')
]