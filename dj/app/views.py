from django.http import HttpResponse
from django.http import Http404
from django.core import serializers
from forms import SongForm
from forms import PlaylistForm
from forms import VoteForm
from forms import AccountForm
from models import Song
from models import Playlist
from models import Account


def _get_playlist_or_404(playlist_id):
    try:
        return Playlist.objects.get(pk=playlist_id)
    except Playlist.DoesNotExist:
        raise Http404("Could not find playlist {0}".format(playlist_id))

def _get_account_or_404(account_id):
    try:
        return Account.objects.get(pk=account_id)
    except Account.DoesNotExist:
        raise Http404("Could not find account {0}".format(account_id))

def _get_song_or_404(song_id):
    try:
        return Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        raise Http404("Could not find song {0}".format(song_id))

def _serialize_obj(obj):
   try:
       j = serializers.serialize('json', [obj, ])
       j = j[0]
   except Exception:
       j = "could not find id {0}".format(obj.id)
   return j


def index(request):
    return HttpResponse("Hello, world. BLAH You're at the dj index.")


# SONGS
def song(request, playlist_id, song_id=None):
    # new song
    current_list = _get_playlist_or_404(playlist_id)
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            s = Song(url=form.cleaned_data['url'],
                     account_id=form.cleaned_data['account_id'],
                     playlist_id=playlist_id)
            s.save()
            return HttpResponse("add_song data {0} for list {1} id {2}".format(form.cleaned_data, playlist_id, s.pk))
    # update song
    if request.method == 'PUT':
        form = SongForm(request.PUT)
        if form.is_valid():
            return HttpResponse("update_song data {0} for list {1}".format(form.cleaned_data, playlist_id))
    # view song
    if request.method == 'GET':
        form = SongForm(request.GET)
        if form.is_valid():
            song = Song.objects.get(pk=form.cleaned_data['id'])
            j = _serialize_obj(song)
            return HttpResponse(j)
    return Http404("add_song failed")


def vote(request, playlist_id):
    current_list = _get_playlist_or_404(playlist_id)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            return HttpResponse("vote data {0} for list {1}".format(form.cleaned_data, playlist_id))
    return Http404("must use post")


# PLAYLIST
def new_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            return HttpResponse("new_playlist data {0} for list {1}".format(form.cleaned_data))
    return Http404("failed new_playlist")


def playlist(request, playlist_id):
        # update playlist
        current_list = _get_playlist_or_404(playlist_id)
        if request.method == 'POST':
            form = PlaylistForm(request.POST)
            if form.is_valid():
                return HttpResponse("update_playlist data {0} for list {1}".format(form.cleaned_data, playlist_id))
        # view playlist
        if request.method == 'GET':
            form = PlaylistForm(request.GET)
            if form.is_valid():
                j = _serialize_obj(current_list)
                return HttpResponse(j)
        return Http404("failed update playlist")


# ACCOUNT
def new_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            return HttpResponse("new_account data {0}".format(form.cleaned_data))
    return Http404("failed new account")


def account(request, account_id):
    current_account = _get_account_or_404(account_id)
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            return HttpResponse("update_account data {0} for account {1}".format(form.cleaned_data, account_id))
    if request.method == 'GET':
        form = AccountForm(request.GET)
        if form.is_valid():
            j = _serialize_obj(current_account)
            return HttpResponse(j)
    return Http404("failed update account")
