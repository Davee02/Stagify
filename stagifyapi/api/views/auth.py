from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls.conf import path
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
import json


@require_http_methods(["POST"])
def register(request):
    try:
        request_user = json.loads(request.body)
        username = request_user['username']
        email = request_user['email']
        password = request_user['password']
        firstname = request_user['firstname']
        lastname = request_user['lastname']

        user = User.objects.create_user(
            username, email, password, first_name=firstname, last_name=lastname)
        response = {"id": user.id, "email": user.email, "username": user.username,
                    "firstname": user.first_name, "lastname": user.last_name}

        return JsonResponse(response)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except IntegrityError as e:
        return JsonResponse({"message": "An user with the same username already exists"}, status=409)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)


@require_http_methods(["POST"])
def logIn(request):
    try:
        request_user = json.loads(request.body)
        username = request_user['username']
        password = request_user['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Authentification was successful"})

        return JsonResponse({"message": 'Invalid credentials supplied'}, status=401)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)


@require_http_methods(["POST"])
def logOut(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)

        logout(request)

        return JsonResponse({"message": "Logging out was successful"})
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)


@require_http_methods(["GET"])
def userInfo(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)

        user = request.user
        response = {"id": user.id, "email": user.email,
                    "username": user.username, "firstname": user.first_name, "lastname": user.last_name}

        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)


urlpatterns = [
    path('user/register', register, name='register'),
    path('user/login', logIn, name='login'),
    path('user/logout', logOut, name='logout'),
    path('user/', userInfo, name='userinfo')
]
