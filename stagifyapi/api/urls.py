from django.urls import path

from .views import auth, test, concert

urlpatterns = [
    path('', test.index, name='index'),
    path('user/register', auth.register, name='register'),
    path('user/login', auth.logIn, name='login'),
    path('user/logout', auth.logOut, name='logout'),
    path('user/', auth.userInfo, name='userinfo'),
    path('concerts/', concert.create_concert, name='create concert'),
    path('concerts/<int:concertId>', concert.read_concert, name='read concert'),
    path('concerts/<int:concertId>/artwork', concert.set_artwork, name='set concert artwork'),
]