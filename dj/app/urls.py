from django.conf.urls import url
from django.conf.urls import include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<list_id>[0-9]+)/add/$', views.add),
    url(r'^new/$', views.new_playlist),
]
