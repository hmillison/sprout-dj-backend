from django.http import Http404
from django.core import serializers
from django.core.exceptions import ObjectDoesNotExist
from models import Song
from models import Account
from models import Playlist
from models import Vote


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

def _serialize_obj(obj):
    try:
        j = serializers.serialize('json', [obj, ])
    except Exception:
        j = "could not find id {0}".format(obj.id)
    return j
