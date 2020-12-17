from django.http import JsonResponse

from ..models import Question


def index(request):
    firstQuestion = Question.objects.first()

    return JsonResponse({"question": firstQuestion.question_text})
