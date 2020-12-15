from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.azure_storage import AzureStorage


def select_storage():
    return FileSystemStorage() if settings.DEBUG else AzureStorage()


class Artist(models.Model):
    displayname = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    avatar = models.FileField(
        upload_to='artist_avatars', storage=select_storage)


class Concert(models.Model):

    class ConcertState(models.IntegerChoices):
        WAITING = 0
        RUNNING = 1

    displayname = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    artwork = models.FileField(
        upload_to='concert_artworks', storage=select_storage)
    startDateTime = models.DateTimeField()
    duration = models.PositiveIntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.DO_NOTHING)
    state = models.IntegerField(
        choices=ConcertState.choices, default=ConcertState.WAITING)
