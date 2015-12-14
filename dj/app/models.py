# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.db import models


class Account(models.Model):
    id = models.IntegerField(primary_key=True)
    slack_name = models.CharField(max_length=256, blank=True, null=True)
    avatar_url = models.TextField(blank=True, null=True)
    is_this_john = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account'


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Playlist(models.Model):
    id = models.IntegerField(primary_key=True)
    slack_room_id = models.CharField(max_length=256, blank=True, null=True)
    url = models.CharField(max_length=1024, blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    now_playing = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'playlist'


class Song(models.Model):
    id = models.IntegerField(primary_key=True)
    url = models.TextField(blank=True, null=True)
    account_id = models.IntegerField(blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    playlist_id = models.IntegerField(blank=True, null=True)
    played_on = models.DateTimeField(blank=True, null=True)
    got_noped = models.IntegerField(blank=True, null=True)
    duration = models.IntegerField(blank=True, null=True)
    paused_at = models.IntegerField(blank=True, null=True)
    is_this_john = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'song'


class Vote(models.Model):
    id = models.IntegerField(primary_key=True)
    song_id = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=32, blank=True, null=True)
    date_added = models.DateTimeField(blank=True, null=True)
    account_id = models.IntegerField(blank=True, null=True)
    on = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'vote'
