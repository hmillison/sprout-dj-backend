from django.http import HttpResponse
from django.http import Http404
from forms import SongForm
from forms import PlaylistForm
from forms import VoteForm
from forms import AccountForm
from models import Account
from models import Song
from models import Vote
from models import Playlist
from helpers import _get_account_or_404
from helpers import _get_playlist_or_404
from helpers import _get_song_or_404
from helpers import _get_vote_or_404
from helpers import _serialize_obj
from urlparse import urlparse,parse_qs
import soundcloud
import urllib
from datetime import datetime


def index(request):
    return HttpResponse("Hello, world. You're at the dj index.")


# SONGS
def song(request, playlist_id, song_id=None):
    # new song
    current_list = _get_playlist_or_404(playlist_id)
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            #check if it's a valid soundcloud or youtube url
            parsedurl = urlparse(form.cleaned_data['url'])

            #for youtube links
            if 'youtu' in parsedurl.netloc:
                qs=parse_qs(parsedurl.query)
                if 'v' in qs:
                    url = 'http://www.youtube.com/watch?v='+qs['v']
                elif len(parsedurl.path) == 12:
                    url = 'http://www.youtube.com/watch?v='+parsedurl.path[1:]
                else:
                    return HttpResponse("This is not a valid Youtube link.")
                artist = ''
                uploader = ''
                title = ''
                duration = 0

            #soundcloud
            elif 'soundcloud' in parsedurl.netloc:
                url = 'http://www.soundcloud.com'+parsedurl.path

                #test if it's a real song
                status = urllib.urlopen(url)

                #if yes...
                if status.getcode() == 200:
                    #create soundcloud and track objects
                    client = soundcloud.Client(client_id='b0686a28dee74e31a989136bb04375ce')
                    track = client.get('/resolve', url=url)

                    #get all song info
                    trackinfo = track.fields()
                    artist = trackinfo['user']['username']
                    uploader = trackinfo['user']['username']
                    title = trackinfo['title']
                    duration = trackinfo['duration']
                else:
                    return HttpResponse("This is not a Soundcloud link.")

            else:
                return HttpResponse("This is not a valid Youtube or Soundcloud link.")

            #check if it already exists on the playlist
            f = Song.objects.filter(url=url,playlist_id=playlist_id).count()

            #if not, do stuff
            if f == 0:
                date_added=datetime.utcnow()
                s = Song(url=url,
                         account_id=form.cleaned_data['account_id'],
                         playlist_id=playlist_id,
                         artist=artist,
                         title=title,
                         uploader=uploader,
                         duration=duration,
                         date_added=date_added
                         )
                s.save()
                return HttpResponse("add_song data {0} for list {1} id {2}".format(form.cleaned_data, playlist_id, s.pk))
            else:
                return HttpResponse("This is on the playlist already, stupid.")
    # update song
    if request.method == 'PUT':
        form = SongForm(request.PUT)
        if form.is_valid():
            return HttpResponse("update_song data {0} for list {1}".format(form.cleaned_data, playlist_id))
    # view song
    if request.method == 'GET':
        form = SongForm(request.GET)
        if form.is_valid():
            song = _get_song_or_404(form.cleaned_data['id'])
            j = _serialize_obj(song)
            return HttpResponse(j)
    return Http404("add_song failed")


def vote(request, playlist_id):
    current_list = _get_playlist_or_404(playlist_id)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():
            v = Vote(type=form.cleaned_data['type'],
                     account_id=form.cleaned_data['account_id'],
                     on=form.cleaned_data['on'])
            v.save()
            j = _serialize_obj(v)
            return HttpResponse(j)
    if request.method == 'GET':
        form = VoteForm(request.POST)
        if form.is_valid():
            v = _get_vote_or_404(form.cleaned_data['id'])
            j = _serialize_obj(v)
            return HttpResponse(j)
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
            a = Account(slack_name=form.cleaned_data['slack_name'],
                        avatar_url=form.cleaned_data['avatar_url'],
                        is_this_john=form.cleaned_data['is_this_john'],
                        slack_id=form.cleaned_data['slack_id'],
                        slack_token=form.cleaned_data['slack_tocken']
                        )
            a.save()
            j = _serialize_obj(a)
            return HttpResponse(j)
    return Http404("failed new account")


def account(request, account_id):
    current_account = _get_account_or_404(account_id)
    if request.method == 'PUT':
        form = AccountForm(request.PUT)
        if form.is_valid():
            return HttpResponse("update_account data {0} for account {1}".format(form.cleaned_data, account_id))
    if request.method == 'GET':
        form = AccountForm(request.GET)
        if form.is_valid():
            j = _serialize_obj(current_account)
            return HttpResponse(j)
    return Http404("failed update account")
