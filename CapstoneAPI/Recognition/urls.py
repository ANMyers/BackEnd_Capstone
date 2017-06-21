from django.conf.urls import url
from Recognition.views import format_dataset, kmeans, my_saved, my_project, delete_project, SVC

app_name = "Recognition"
urlpatterns = [
    url(r'^kmeans/$', kmeans, name='kmeans'),
    url(r'^svc/$', SVC, name='svc'),
    url(r'^format_dataset/$', format_dataset, name='format_dataset'),
    url(r'^my_saved/$', my_saved, name='my_saved'),
    url(r'^delete_project/$', delete_project, name='delete_project'),
    url(r'^my_project/$', my_project, name='my_project')
]