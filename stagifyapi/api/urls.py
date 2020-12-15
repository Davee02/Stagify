from django.urls import path

from .views import auth, concert, artist

urlpatterns = auth.urlpatterns + concert.urlpatterns + artist.urlpatterns
