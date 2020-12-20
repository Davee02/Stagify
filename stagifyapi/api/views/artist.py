import json
from django.contrib.auth.models import User
from django.db.models import Q
from django.http.response import JsonResponse
from django.urls.conf import path
from django.views.decorators.http import require_http_methods
from ..models import Artist
import uuid


@require_http_methods(["GET", "POST", "PUT"])
def index(request):
    if request.method == "POST":
        return create_artist(request)
    elif request.method == "PUT":
        return update_artist(request)
    elif request.method == "GET":
        return read_all(request)

@require_http_methods(["POST"])
def create_artist(request):
    try:
        if not request.user.is_authenticated or not request.user.is_staff:
            return JsonResponse({"message": 'Unauthorized'}, status=401)

        request_artist = json.loads(request.body)
        displayname = request_artist['displayname']
        description = request_artist['description']
        userId = int(request_artist['userId'])

        user = User.objects.get(id=userId)

        newArtist = Artist(displayname=displayname, description=description, userId=user)
        newArtist.save()

        return JsonResponse({"message": "Successfully created artist"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except User.DoesNotExist:
        return JsonResponse({"message": 'The specified user does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

@require_http_methods(["GET"])
def read_all(request):
    try:
        artists = Artist.objects.values(
            "id", "displayname", "description", "avatar").all()

        return JsonResponse(list(artists), safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

@require_http_methods(["POST"])
def set_avatar(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)

        user = User.objects.get(username=request.user.username)        
        artist = Artist.objects.get(userId=user)
        artist.avatar = request.FILES["avatar"]
        artist.avatar.name = '%s%s' % (uuid.uuid4(), artist.avatar.name)
        artist.save()

        return JsonResponse({"message": "Successfully updated artist avatar"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Artist.DoesNotExist:
        return JsonResponse({"message": 'Unauthorized'}, status=401)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

@require_http_methods(["PUT"])
def update_artist(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)

        request_artist = json.loads(request.body)
        displayname = request_artist['displayname']
        description = request_artist['description']

        user = User.objects.get(username=request.user.username)
        artist = Artist.objects.get(userId=user)

        artist.displayname = displayname
        artist.description = description
        artist.save()

        return JsonResponse({"message": "Successfully updated artist"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Artist.DoesNotExist:
        return JsonResponse({"message": 'Unauthorized'}, status=401)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

@require_http_methods(["GET"])
def read_artist(request, artistId):
    try:
        artists = Artist.objects.values(
            "id", "displayname", "description", "avatar").get(pk=artistId)

        return JsonResponse(artists, safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Artist.DoesNotExist:
        return JsonResponse({"message": 'The specified artist does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

@require_http_methods(["GET"])
def by_searchterm(request, searchTerm):
    try:
        artists = Artist.objects.values(
            "id", "displayname", "description", "avatar").filter(Q(displayname__icontains=searchTerm) | Q(description__icontains=searchTerm))

        return JsonResponse(list(artists), safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Artist.DoesNotExist:
        return JsonResponse({"message": 'The specified artist does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)

urlpatterns = [
    path('artists/', index, name='create, update or read artists'),
    path('artists/avatar', set_avatar, name='set avatar'),
    path('artists/<int:artistId>', read_artist,
        name='read artist'),
    path('artists/search/<searchTerm>', by_searchterm,
        name='search for artist'),
]
