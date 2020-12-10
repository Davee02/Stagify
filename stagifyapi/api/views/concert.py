import json
import random
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from ..models import Concert
import uuid

@require_http_methods(["GET", "POST"])
def index(request):
    if request.method == "POST":
        return create_concert(request)
    elif request.method == "GET":
        return read_all(request)

@require_http_methods(["GET", "PUT"])
def concert_id(request, concertId):
    if request.method == "PUT":
        return update_concert(request, concertId)
    elif request.method == "GET":
        return read_concert(request, concertId)

@require_http_methods(["POST"])
def create_concert(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)
        
        request_concert = json.loads(request.body)
        displayname = request_concert['displayname']
        description = request_concert['description']

        newConcert = Concert(displayname=displayname, description=description)
        newConcert.save()

        return JsonResponse({"message": "Successfully created concert"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse({"message": 'The specified concert does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

@require_http_methods(["GET"])
def read_concert(request, concertId):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)
        
        concert = Concert.objects.values("id", "displayname", "description", "artwork").get(pk=concertId)

        return JsonResponse(concert, safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse({"message": 'The specified concert does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

@require_http_methods(["PUT"])
def update_concert(request, concertId):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)
        
        request_concert = json.loads(request.body)
        displayname = request_concert['displayname']
        description = request_concert['description']

        concert = Concert.objects.get(pk=concertId)

        concert.displayname = displayname
        concert.description = description
        concert.save()

        return JsonResponse({"message": "Successfully updated concert"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse({"message": 'The specified concert does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

@require_http_methods(["GET"])
def read_all(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)
        
        concerts = Concert.objects.values("id", "displayname", "description", "artwork").all()

        return JsonResponse(list(concerts), safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse({"message": 'The specified concert does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

@require_http_methods(["GET"])
def suggestions(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)
        
        suggestions_count = int(request.GET.get("count", 5))
        all_concerts = Concert.objects.values("id", "displayname", "description", "artwork").all()
        random_items = random.sample(list(all_concerts), suggestions_count)

        return JsonResponse(random_items, safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse({"message": 'The specified concert does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

@require_http_methods(["POST"])
def set_artwork(request, concertId):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)
        
        concert = Concert.objects.get(pk=concertId)
        concert.artwork = request.FILES["artwork"]
        concert.artwork.name = '%s%s' % (uuid.uuid4(), concert.artwork.name)
        concert.save()

        return JsonResponse({"message": "Successfully updated concert artwork"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse({"message": 'The specified concert does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)