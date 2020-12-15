import json
import random
from django.http.response import JsonResponse
from django.urls.conf import path
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods
from ..models import Artist, Concert
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
        duration = int(request_concert['duration'])
        artistId = int(request_concert['artist'])
        startDateTime = parse_datetime(request_concert['startDateTime'])

        artist = Artist.objects.get(pk=artistId)

        newConcert = Concert(displayname=displayname, description=description,
                             duration=duration, startDateTime=startDateTime, artist=artist)
        newConcert.save()

        return JsonResponse({"message": "Successfully created concert"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Artist.DoesNotExist:
        return JsonResponse({"message": 'The specified artist does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)


@require_http_methods(["GET"])
def read_concert(request, concertId):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)

        concert = Concert.objects.values(
            "id", "displayname", "description", "artwork", "duration", "startDateTime", "artist", "state").get(pk=concertId)

        return JsonResponse(concert, safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse({"message": 'The specified concert does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

@require_http_methods(["GET"])
def by_artist(request, artistId):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)

        artist = Artist.objects.get(pk=artistId)
        concert = Concert.objects.values(
            "id", "displayname", "description", "artwork", "duration", "startDateTime", "artist", "state").filter(artist=artist)

        return JsonResponse(list(concert), safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Artist.DoesNotExist:
        return JsonResponse({"message": 'The specified artist does not exist'}, status=404)
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
        duration = int(request_concert['duration'])
        artistId = int(request_concert['artist'])
        state = int(request_concert['state'])
        startDateTime = parse_datetime(request_concert['startDateTime'])

        if state not in Concert.ConcertState.values:
            return JsonResponse({"message": "Invalid state"}, status=400)

        concert = Concert.objects.get(pk=concertId)
        artist = Artist.objects.get(pk=artistId)

        concert.displayname = displayname
        concert.description = description
        concert.duration = duration
        concert.startDateTime = startDateTime
        concert.artist = artist
        concert.state = state
        concert.save()

        return JsonResponse({"message": "Successfully updated concert"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse({"message": 'The specified concert does not exist'}, status=404)
    except Artist.DoesNotExist:
        return JsonResponse({"message": 'The specified artist does not exist. No changes were made'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)


@require_http_methods(["GET"])
def read_all(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)

        concerts = Concert.objects.values(
            "id", "displayname", "description", "artwork", "duration", "startDateTime", "artist", "state").all()

        return JsonResponse(list(concerts), safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)


@require_http_methods(["GET"])
def suggestions(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)

        suggestions_count = int(request.GET.get("count", 5))
        all_concerts = Concert.objects.values(
            "id", "displayname", "description", "artwork", "duration", "startDateTime", "artist", "state").all()
        random_items = random.sample(list(all_concerts), suggestions_count)

        return JsonResponse(random_items, safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)


@require_http_methods(["PUT"])
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


urlpatterns = [
    path('concerts/', index,
         name='index endpoint - create new concert or list all'),
    path('concerts/suggestions', suggestions,
         name='concert suggestions for user'),
    path('concerts/<int:concertId>', concert_id,
         name='read or update concert'),
    path('concerts/artist/<int:artistId>', by_artist,
         name='read concerts by artist'),
    path('concerts/<int:concertId>/artwork',
         set_artwork, name='set concert artwork')
]
