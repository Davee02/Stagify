import json
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from ..models import Artist

@require_http_methods(["POST"])
def create_artist(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)

        request_artist = json.loads(request.body)
        displayname = request_artist['displayname']
        description = request_artist['description']

        newArtist = Artist(displayname=displayname, description=description)
        newArtist.save()

        return JsonResponse({"message": "Successfully created artist"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)