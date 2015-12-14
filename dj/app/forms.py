from django import forms


class SongForm(forms.Form):
    id = forms.IntegerField(required=False)
    account_id = forms.IntegerField(required=True)
    link = forms.CharField(required=True)
    time_played = forms.IntegerField(required=False)
    durration = forms.IntegerField(required=False)
    got_noped = forms.IntegerField(required=False)
    time_passed = forms.IntegerField(required=False)
    is_this_john = forms.BooleanField(required=False)

class PlaylistForm(forms.Form):
    id = forms.IntegerField(required=False)
    time_start = forms.IntegerField(required=False)
    time_end = forms.IntegerField(required=False)
    now_playing = forms.IntegerField(required=False)

class VoteForm(forms.Form):
    song_id = forms.IntegerField(required=True)
    type = forms.CharField(required=True)
    account_id = forms.IntegerField(required=True)
    on = forms.BooleanField(required=False)

class AccountForm(forms.Form):
    id = forms.IntegerField(required=False)
    slack_name = forms.CharField(required=False)
    url_to_jpeg = forms.CharField(required=False)
    is_this_john = forms.BooleanField(required=False)
