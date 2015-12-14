from django.http import Http404
from django.core import serializers
from models import Song
from models import Account
from models import Playlist

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
