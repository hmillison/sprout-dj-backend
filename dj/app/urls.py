from django.conf.urls import url
from django.conf.urls import include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #songs
    url(r'^(?P<list_id>[0-9]+)/song/$', views.song),
    url(r'^(?P<list_id>[0-9]+)/vote/$', views.vote),
    # playlist
    url(r'^(?P<list_id>[0-9]+)/playlist/$', views.playlist),
    url(r'^new_playlist/$', views.new_playlist),
    # account
    url(r'^new_account/$', views.new_account),
    url(r'^(?P<account_id>[0-9]+)/account/$', views.account),
]
