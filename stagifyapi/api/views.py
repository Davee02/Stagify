from django.http import HttpResponse, HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import json

from .models import Question

def index(request):
    firstQuestion = Question.objects.first()

    return HttpResponse(firstQuestion.question_text)

def register(request):
    if request.method == 'POST':
        request_user = json.loads(request.body)
        try:
            username = request_user['username']
            email = request_user['email']
            password = request_user['password']

            user = User.objects.create_user(username, email, password)
            return HttpResponse(user)
        except KeyError:
            return HttpResponseServerError("Malformed data!")

    return HttpResponseNotFound()

def logIn(request):
    if request.method == 'POST':
        request_user = json.loads(request.body)
        try:
            username = request_user['username']
            password = request_user['password']

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("Authentification was successful")

            return HttpResponse('Invalid credentials supplied', status=401)
        except KeyError:
            return HttpResponseServerError("Malformed data!")

    return HttpResponseNotFound()

def logOut(request):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponse('Unauthorized', status=401)

        logout(request)
        return HttpResponse("Logging out was successful")

    return HttpResponseNotFound()

def userInfo(request):
    if not request.user.is_authenticated:
        return HttpResponse('Unauthorized', status=401)

    return HttpResponse(request.user.email)
