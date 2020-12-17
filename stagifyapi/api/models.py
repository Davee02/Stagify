from django.db import models
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from storages.backends.azure_storage import AzureStorage

def select_storage():
    return FileSystemStorage() if settings.DEBUG else AzureStorage()

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

class Concert(models.Model):
    displayname = models.CharField(max_length=500)
    description = models.CharField(max_length=10000)
    artwork = models.FileField(upload_to='concert_artworks', storage=select_storage)