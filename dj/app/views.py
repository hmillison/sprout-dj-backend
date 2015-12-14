from django.http import HttpResponse
from django.http import Http404
from forms import SongForm
from forms import PlaylistForm
from forms import VoteForm
from forms import AccountForm
from models import Song

def index(request):
    return HttpResponse("Hello, world. BLAH You're at the dj index.")


# SONGS
def add_song(request, list_id):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            s = Song(url=form.cleaned_data['url'],
                     account_id=form.cleaned_data['account_id'],
                     playlist_id=list_id)
            s.save()
            return HttpResponse("add_song data {0} for list {1} id {2}".format(form.cleaned_data, list_id, s.pk))
    return Http404("add_song failed")


def vote(request, list_id):
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            return HttpResponse("vote data {0} for list {1}".format(form.cleaned_data, list_id))
    return Http404("must use post")


def update_song(request, list_id):
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            return HttpResponse("update_song data {0} for list {1}".format(form.cleaned_data, list_id))
    return Http404("update_song failed")


# PLAYLIST
def new_playlist(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            return HttpResponse("new_playlist data {0} for list {1}".format(form.cleaned_data))
    return Http404("failed new_playlist")


def update_playlist(request, list_id):
        if request.method == 'POST':
            form = PlaylistForm(request.POST)
            if form.is_valid():
                return HttpResponse("update_playlist data {0} for list {1}".format(form.cleaned_data, list_id))
        return Http404("failed update playlist")


# ACCOUNT
def new_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            return HttpResponse("new_account data {0}".format(form.cleaned_data))
    return Http404("failed new account")


def update_account(request, account_id):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            return HttpResponse("update_account data {0} for account {1}".format(form.cleaned_data, account_id))
    return Http404("failed update account")
