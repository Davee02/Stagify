from django.urls import path

from .views import auth, test

urlpatterns = [
    path('', test.index, name='index'),
    path('user/register', auth.register, name='register'),
    path('user/login', auth.logIn, name='login'),
    path('user/logout', auth.logOut, name='logout'),
    path('user', auth.userInfo, name='userinfo'),
]