from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls.conf import path
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from ..models import Artist
import json


def validate_userinfo(username, email, password, firstname, lastname):
    if not username:
        return False, "Username must not be empty"

    if not email:
        return False, "Email must not be empty"

    if not "@" in email:
        return False, "Email must be a valid email address"

    if not password:
        return False, "Password must not be empty"

    if len(password) < 8:
        return False, "Password must be at least 8 characters long"

    if not firstname:
        return False, "Firstname must not be empty"

    if not lastname:
        return False, "Lastname must not be empty"

    return True, None


@require_http_methods(["GET", "PUT"])
def index(request):
    if request.method == "PUT":
        return update_info(request)
    elif request.method == "GET":
        return userInfo(request)


@require_http_methods(["POST"])
def register(request):
    try:
        request_user = json.loads(request.body)
        username = request_user["username"]
        email = request_user["email"]
        password = request_user["password"]
        firstname = request_user["firstname"]
        lastname = request_user["lastname"]

        userinfo_valid, validation_error = validate_userinfo(
            username, email, password, firstname, lastname
        )
        if not userinfo_valid:
            return JsonResponse({"message": validation_error}, status=400)

        user = User.objects.create_user(
            username, email, password, first_name=firstname, last_name=lastname
        )
        response = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "firstname": user.first_name,
            "lastname": user.last_name,
        }

        return JsonResponse(response)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except IntegrityError as e:
        return JsonResponse(
            {"message": "An user with the same username already exists"}, status=409
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["PUT"])
def update_info(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        request_user = json.loads(request.body)
        username = request_user["username"]
        email = request_user["email"]
        password = request_user["password"]
        firstname = request_user["firstname"]
        lastname = request_user["lastname"]

        userinfo_valid, validation_error = validate_userinfo(
            username, email, password, firstname, lastname
        )
        if not userinfo_valid:
            return JsonResponse({"message": validation_error}, status=400)

        user = User.objects.get(username=request.user.username)
        user.set_password(password)
        user.username = username
        user.email = email
        user.first_name = firstname
        user.last_name = lastname

        user.save()

        return JsonResponse({"message": "Successfully changed user info"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except IntegrityError as e:
        return JsonResponse(
            {"message": "An user with the same username already exists"}, status=409
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["POST"])
def logIn(request):
    try:
        request_user = json.loads(request.body)
        username = request_user["username"]
        password = request_user["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Authentification was successful"})

        return JsonResponse({"message": "Invalid credentials supplied"}, status=401)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["POST"])
def logOut(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        logout(request)

        return JsonResponse({"message": "Logging out was successful"})
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["GET"])
def userInfo(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        user = request.user

        artist_id = 0

        try:
            artist = Artist.objects.get(userId=user)
            artist_id = artist.id
        except Artist.DoesNotExist:
            artist_id = None

        response = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "firstname": user.first_name,
            "lastname": user.last_name,
            "artistId": artist_id,
        }

        return JsonResponse(response)
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


urlpatterns = [
    path("user/register", register, name="register"),
    path("user/login", logIn, name="login"),
    path("user/logout", logOut, name="logout"),
    path("user/", index, name="get or update userinfo"),
]
