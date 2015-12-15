from django.http import Http404
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from models import Song
from models import Account
from models import Playlist
from models import Vote
import json


def _get_playlist_or_404(playlist_id):
    try:
        return Playlist.objects.get(pk=playlist_id)
    except ObjectDoesNotExist:
        print("Could not find playlist {0}".format(playlist_id))
        raise Http404

def _get_account_or_404(account_id):
    try:
        return Account.objects.get(pk=account_id)
    except ObjectDoesNotExist:
        print("Could not find account {0}".format(account_id))
        raise Http404


def _get_song_or_404(song_id):
    try:
        return Song.objects.get(pk=song_id)
    except ObjectDoesNotExist:
        print("Could not find song {0}".format(song_id))
        raise Http404

def _get_vote_or_404(vote_id):
    try:
        return Vote.objects.get(pk=vote_id)
    except ObjectDoesNotExist:
        print("Could not find vote {0}".format(vote_id))
        raise Http404

def _serialize_obj(obj, is_string=True):
    try:
        j = obj.__dict__
        j.pop('_state', None)
        if j.get('date_added'):
            j['date_added'] = "{0}".format(j['date_added'])
    except Exception:
        j = {}
    if is_string:
        # j = serializers.serialize('json', [j, ])
        j = json.dumps(j)
    return j

def _serialize_all_obj(objs, is_string=True):
    try:
        j = []
        for o in objs:
            tmp = o.__dict__
            tmp.pop('_state', None)
            if tmp.get('date_time'):
                tmp['date_time'] = "{0}".format(tmp['date_time'])
            j.append(tmp)
    except Exception:
        j = []
    if is_string:
        # j = serializers.serialize('json', j)
        j = json.dump(j)
    return j


def _format_song(song, is_string=False):
    votes = Vote.objects.filter(song_id=song.id)
    format = {}
    format['song'] = _serialize_obj(song, is_string=False)
    format['votes'] = _serialize_all_obj(votes, is_string=False)
    if is_string:
        format = json.dumps(format)
    return format
