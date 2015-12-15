from django.conf.urls import url
from django.conf.urls import include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #songs
    url(r'^(?P<playlist_id>[0-9]+)/song/$', views.song),
    url(r'^(?P<playlist_id>[0-9]+)/song/all/$', views.all_songs),
    url(r'^(?P<playlist_id>[0-9]+)/vote/$', views.vote),
    # playlist
    url(r'^playlist/$', views.playlist),
    # account
    url(r'^account/$', views.account),
]
