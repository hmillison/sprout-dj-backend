from django.http import HttpResponse
from django.http import Http404
from django.http import HttpResponseBadRequest
from forms import SongForm
from forms import PlaylistForm
from forms import VoteForm
from forms import AccountForm
from models import Account
from models import Song
from models import Vote
from models import Playlist
from django.db.models import F
from helpers import _get_account_or_404
from helpers import _get_playlist_or_404
from helpers import _get_song_or_404
from helpers import _get_vote_or_404
from helpers import _serialize_obj
from helpers import _serialize_all_obj
from helpers import _format_song
from helpers import _update_object
from urlparse import urlparse
from urlparse import parse_qs
import soundcloud
import urllib
import requests
import json
from datetime import datetime
import isodate
import logging

logger = logging.getLogger(__name__)


def index(request):
    return HttpResponse("Hello, world. You're at the dj index.")


# SONGS
def song(request, playlist_id):
    # new song
    current_list = _get_playlist_or_404(playlist_id)
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            #check if it's a valid soundcloud or youtube url
            parsedurl = urlparse(form.cleaned_data['url'])

            if not form.cleaned_data.get('account_id'):
                logger.error("No account passed in for new song")
                return HttpResponseBadRequest("Please use a valid account.")
            else:
                #check for account
                account = _get_account_or_404(form.cleaned_data['account_id'])

            #for youtube links
            if 'youtu' in parsedurl.netloc:
                qs=parse_qs(parsedurl.query)

                #check if it's a shortened link and figure out the id
                if 'v' in qs:
                    ytid = qs['v'][0]
                    url = 'http://www.youtube.com/watch?v=' + ytid
                elif len(parsedurl.path) == 12:
                    ytid = parsedurl.path[1:]
                    url = 'http://www.youtube.com/watch?v=' + ytid
                else:
                    logger.error("Not a valid youtube link, request {0}".format(form.cleaned_data))
                    return HttpResponseBadRequest("This is not a valid Youtube link.")


                #pull track info from YT API
                infourl = 'https://www.googleapis.com/youtube/v3/videos?id=' + ytid + '&key=AIzaSyCrUdVGALPgTv4zguqksg835EK3mRPhpfE&fields=items(id,snippet,contentDetails)&part=snippet,contentDetails'

                trackinfo = requests.get(infourl).json()

                artist = trackinfo['items'][0]['snippet']['channelTitle']
                uploader = trackinfo['items'][0]['snippet']['channelTitle']
                title = trackinfo['items'][0]['snippet']['localized']['title']
                duration = int(round(isodate.parse_duration(trackinfo['items'][0]['contentDetails']['duration']).total_seconds()*1000))

                #if it's more than 30 minutes, replace with rickroll
                if duration > 1800000:
                    url = 'http://www.youtube.com/watch?v=dQw4w9WgXcQ'


                if 'high' in trackinfo['items'][0]['snippet']['thumbnails']:
                    thumbnail = trackinfo['items'][0]['snippet']['thumbnails']['high']['url']
                else:
                    thumbnail = trackinfo['items'][0]['snippet']['thumbnails']['default']['url']

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

                    #if it's more than 30 minutes, replace with rickroll
                    if duration > 1800000:
                        url = 'http://www.youtube.com/watch?v=dQw4w9WgXcQ'

                    #thumbnail
                    if trackinfo['artwork_url']:
                        thumbnail = trackinfo['artwork_url']
                    else:
                        thumbnail = trackinfo['user']['avatar_url']
                else:
                    logger.error("Not a valid soundcloud link, request {0}".format(form.cleaned_data))
                    return HttpResponseBadRequest("This is not a Soundcloud link.")

            else:
                logger.error("This is not a valid Youtube or Soundcloud link. request {0}".format(form.cleaned_data))
                return HttpResponseBadRequest("This is not a valid Youtube or Soundcloud link.")

            #check if it already exists on the playlist
            f = Song.objects.filter(url=url,playlist_id=playlist_id).count()

            #if not, add to db
            if f == 0:
                date_added=datetime.utcnow()
                s = Song(url=url,
                         account_id=account.id,
                         playlist_id=current_list.id,
                         artist=artist,
                         title=title,
                         uploader=uploader,
                         duration=duration,
                         date_added=date_added,
                         thumbnail=thumbnail
                         )
                s.save()
                j = _serialize_obj(s)
                logger.info("Added new song {0}".format(j))
                return HttpResponse(j)
            else:
                logger.error("This is on the playlist already, stupid. request {0}".format(form.cleaned_data))
                return HttpResponseBadRequest("This is on the playlist already, stupid.")
    # view song
    if request.method == 'GET':
        form = SongForm(request.GET)
        if form.is_valid():
            song = _get_song_or_404(form.cleaned_data['id'])
            j = _format_song(song, is_string=True)
            return HttpResponse(j)
    return Http404("add_song failed")


def song_update(request, playlist_id):
    # update song
    current_list = _get_playlist_or_404(playlist_id)
    if request.method == 'POST':
        form = SongForm(request.POST)
        if form.is_valid():
            current_song = _get_song_or_404(form.cleaned_data['id'])
            if current_song.playlist_id != current_list.id:
                logger.error("The song_update {0} is not part of playlist {1}, request {2}".format(song.id, current_list.id, form.cleaned_data))
                return HttpResponseBadRequest("this song is not for the current playlist")
            _update_object(current_song, form.cleaned_data)
            return HttpResponse("update_song data")


def all_songs(request, playlist_id):
    if request.method == 'GET':
        current_list = _get_playlist_or_404(playlist_id)
        all = Song.objects.filter(playlist_id=current_list.id).select_related()
        ar = []
        for a in all:
            ar.append(_format_song(a))
        return HttpResponse(json.dumps(ar))
    return Http404("all_song failed")


def vote(request, playlist_id):
    current_list = _get_playlist_or_404(playlist_id)
    if request.method == 'POST':
        form = VoteForm(request.POST)
        if form.is_valid():

            if not form.cleaned_data.get('account_id'):
                return HttpResponse("Please use a valid account.",status='401')
            else:
                #check for account
                account_id = form.cleaned_data['account_id']
                if not _get_account_or_404(account_id):
                    return HttpResponse("Please use a valid account.",status='401')

            type = form.cleaned_data['type']
            on=form.cleaned_data['on']
            song_id=form.cleaned_data['song_id']

            #check if vote exists
            v = Vote.objects.filter(account_id=account_id,song_id=song_id)
            f = v.values()

            #if so, check if on
            if len(f) > 1:
                logger.error("You done fucked up, request {0}".format(form.cleaned_data))
                return HttpResponseBadRequest("You done fucked up somehow.")
            elif len(f) == 1:
                if f[0]['type'] <> type or f[0]['on'] <> on:
                    v.update(on=on,type=type)
                    j = _serialize_obj(v[0])
                elif f[0]['on'] == 1 and on==1:
                    logger.error("You already voted on this track, jerk, request {0}".format(form.cleaned_data))
                    return HttpResponseBadRequest("You already voted on this track, jerk.")
                elif f[0]['on'] == 0 and on==0:
                    logger.error("You already unvoted on this track, jerk, request {0}".format(form.cleaned_data))
                    return HttpResponseBadRequest("You already unvoted this track, jerk.")
            else:
                date_added=datetime.utcnow()
                #if not exists add
                v = Vote(type=type,
                         account_id=account_id,
                         on=on,
                         song_id=song_id,
                         date_added=date_added
                         )
                v.save()
                j = _serialize_obj(v)
                logger.info("Added new vote {0}".format(j))

            #check nope threshold here

            #return row
            return HttpResponse(j)
    if request.method == 'GET':
        form = VoteForm(request.POST)
        if form.is_valid():
            v = _get_vote_or_404(form.cleaned_data['id'])
            j = _serialize_obj(v)
            return HttpResponse(j)
    return Http404("must use post")


# PLAYLIST
def playlist(request):
        # add playlist
        if request.method == 'POST':
            form = PlaylistForm(request.POST)
            if form.is_valid():
                p = Playlist(url=form.cleaned_data['url'],
                             slack_room_id=form.cleaned_data['slack_room_id'],
                             date_added=datetime.utcnow())
                p.save()
                j = _serialize_obj(p)
                logger.info("Added playlist {0}".format(j))
                return HttpResponse(j)
        # view playlist
        if request.method == 'GET':
            form = PlaylistForm(request.GET)
            if form.is_valid():
                current_list = _get_playlist_or_404(form.cleaned_data['id'])
                j = _serialize_obj(current_list)
                return HttpResponse(j)
        return Http404("failed update playlist")


def playlist_update(request):
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            current_list = _get_playlist_or_404(form.cleaned_data['id'])
            if not form.cleaned_data.get('now_playing'):
                logger.error("No song present to add, request {0}".format(form.cleaned_data))
                return HttpResponseBadRequest("cannot update playist without song")
            song = _get_song_or_404(form.cleaned_data['now_playing'])
            if song.playlist_id != current_list.id:
                logger.error("The song {0} is not part of playlist {1}, request {2}".format(song.id, current_list.id, form.cleaned_data))
                return HttpResponseBadRequest("this song is not for the current playlist")
            _update_object(current_list, form.cleaned_data)
            return HttpResponse("updated playlist")


# ACCOUNT
def account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = Account.objects.filter(slack_id=form.cleaned_data['slack_id'])
            if len(account) > 0:
                _update_object(account[0], form.cleaned_data)
            else:
                account = Account(slack_name=form.cleaned_data['slack_name'],
                            avatar_url=form.cleaned_data['avatar_url'],
                            is_this_john=form.cleaned_data['is_this_john'],
                            slack_id=form.cleaned_data['slack_id'],
                            slack_token=form.cleaned_data['slack_token']
                            )
                account.save()
                j = _serialize_obj(account)
                logger.info("New account {0}".format(j))
            return HttpResponse()
    if request.method == 'GET':
        form = AccountForm(request.GET)
        if form.is_valid():
            current_account = _get_account_or_404(form.cleaned_data['id'])
            j = _serialize_obj(current_account)
            return HttpResponse(j)
    return Http404("failed account")


def account_update(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            current_account = _get_account_or_404(form.cleaned_data['id'])
            _update_object(current_account, form.cleaned_data)
            return HttpResponse("update_account data")
    return Http404("failed update account")
