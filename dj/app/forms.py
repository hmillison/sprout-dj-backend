from django import forms


class SongForm(forms.Form):
    id = forms.IntegerField(required=False)
    account_id = forms.IntegerField(required=False)
    url = forms.CharField(required=False)
    time_played = forms.IntegerField(required=False)
    duration = forms.IntegerField(required=False)
    got_noped = forms.IntegerField(required=False)
    time_passed = forms.IntegerField(required=False)
    is_this_john = forms.BooleanField(required=False)
    played_on = forms.DateTimeField(required=False)

class PlaylistForm(forms.Form):
    id = forms.IntegerField(required=False)
    now_playing = forms.IntegerField(required=False)
    url = forms.CharField(required=False)
    slack_room_id = forms.CharField(required=False)

class VoteForm(forms.Form):
    song_id = forms.IntegerField(required=True)
    type = forms.CharField(required=True)
    account_id = forms.IntegerField(required=True)
    on = forms.IntegerField(required=True)

class AccountForm(forms.Form):
    id = forms.IntegerField(required=False)
    slack_name = forms.CharField(required=False)
    avatar_url = forms.CharField(required=False)
    is_this_john = forms.BooleanField(required=False)
    slack_id = forms.CharField(required=False)
    slack_token = forms.CharField(required=False)
