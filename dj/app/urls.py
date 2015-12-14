from django.conf.urls import url
from django.conf.urls import include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    #songs
    url(r'^(?P<list_id>[0-9]+)/add_song/$', views.add_song),
    url(r'^(?P<list_id>[0-9]+)/update_song/$', views.update_song),
    url(r'^(?P<list_id>[0-9]+)/vote/$', views.vote),
    # playlist
    url(r'^(?P<list_id>[0-9]+)/update_playlist/$', views.update_playlist),
    url(r'^new_playlist/$', views.new_playlist),
    # account
    url(r'^new_account/$', views.new_account),
    url(r'^(?P<account_id>[0-9]+)/update_account/$', views.update_account),
]
