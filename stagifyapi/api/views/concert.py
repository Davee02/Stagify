import json
from django.http.response import JsonResponse
from django.views.decorators.http import require_http_methods
from ..models import Concert

@require_http_methods(["POST"])
def create_concert(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": 'Unauthorized'}, status=401)
        
        request_user = json.loads(request.body)
        displayname = request_user['displayname']
        description = request_user['description']

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
        
        concert = Concert.objects.get(pk=concertId)
        response = {"id": concert.id, "displayname": concert.displayname, "description": concert.description, "artwork": concert.artwork.url if concert.artwork else None}

        return JsonResponse(response)
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
        concert.save()

        return JsonResponse({"message": "Successfully updated concert artwork"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse({"message": 'The specified concert does not exist'}, status=404)
    except Exception as e:
        return JsonResponse({"message": "An unexpected error happened: " + str(e)}, status=500)