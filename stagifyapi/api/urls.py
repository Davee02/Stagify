from django.urls import path

from .views import auth, concert, artist

urlpatterns = [
    path('user/register', auth.register, name='register'),
    path('user/login', auth.logIn, name='login'),
    path('user/logout', auth.logOut, name='logout'),
    path('user/', auth.userInfo, name='userinfo'),
    path('concerts/', concert.index,
         name='index endpoint - create new concert or list all'),
    path('concerts/suggestions', concert.suggestions,
         name='concert suggestions for user'),
    path('concerts/<int:concertId>', concert.concert_id,
         name='read or update concert'),
    path('concerts/<int:concertId>/artwork',
         concert.set_artwork, name='set concert artwork'),

    path('artists/',
         artist.create_artist, name='create artist'),
]
