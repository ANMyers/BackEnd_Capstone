from django.conf.urls import url
from Recognition.views import format_dataset, kmeans

app_name = "Recognition"
urlpatterns = [
    url(r'^kmeans/$', kmeans, name='kmeans'),
    url(r'^format_dataset/$', format_dataset, name='format_dataset')
]