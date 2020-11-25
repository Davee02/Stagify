from django.shortcuts import render
from django.http import HttpResponse

from .models import Question

# Create your views here.
def index(request):
    firstQuestion = Question.objects.first()

    return HttpResponse(firstQuestion.question_text)