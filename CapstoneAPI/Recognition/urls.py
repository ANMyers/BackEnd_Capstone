from django.conf.urls import url
from Recognition.views import validate_compatibilty, kmeans

app_name = "Recognition"
urlpatterns = [
    url(r'^kmeans/$', kmeans, name='kmeans'),
    url(r'^validate_compatibilty/$', validate_compatibilty, name='validate_compatibilty')
]