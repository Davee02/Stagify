from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.azure_storage import AzureStorage


def select_storage():
    return FileSystemStorage() if settings.DEBUG else AzureStorage()


class Artist(models.Model):
    displayname = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    userId = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    avatar = models.FileField(
        upload_to='artist_avatars', storage=select_storage)
    avatarUrl = models.URLField()


class Concert(models.Model):
    displayname = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    artwork = models.FileField(
        upload_to='concert_artworks', storage=select_storage)
    artworkUrl = models.URLField()
    startDateTime = models.DateTimeField()
    duration = models.PositiveIntegerField()
    artist = models.ForeignKey(Artist, on_delete=models.DO_NOTHING)


class PurchaseOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    concert = models.ForeignKey(Concert, on_delete=models.DO_NOTHING)
    purchaseDateTime = models.DateTimeField()
