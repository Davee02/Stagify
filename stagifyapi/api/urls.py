from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('user/register', views.register, name='register'),
    path('user/login', views.logIn, name='login'),
    path('user/logout', views.logOut, name='logout'),
    path('user', views.userInfo, name='userinfo'),
]