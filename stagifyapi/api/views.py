from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
import json

from .models import Question


def index(request):
    firstQuestion = Question.objects.first()

    return JsonResponse({"question": firstQuestion.question_text})


@require_http_methods(["POST"])
def register(request):
    try:
        request_user = json.loads(request.body)
        username = request_user['username']
        email = request_user['email']
        password = request_user['password']

        user = User.objects.create_user(username, email, password)
        response = {"id": user.id, "email": user.email, "username": user.username}
        
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

        response = {"id": request.user.id, "email": request.user.email, "username": request.user.username}
        return JsonResponse(response)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)
