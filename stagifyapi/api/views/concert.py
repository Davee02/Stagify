import datetime
import json
import random
from django.contrib.auth.models import User
from django.db.models.query_utils import Q
from django.http.response import JsonResponse
from django.urls.conf import path
from django.db.models import F
from django.utils.dateparse import parse_datetime
from django.views.decorators.http import require_http_methods
from django.core.mail import send_mail
from ..models import Artist, Concert, PurchaseOrder
import uuid


def validate_concert(displayname, description, duration, startDateTime):
    if not displayname:
        return False, "Displayname must not be empty"

    if not description:
        return False, "Description must not be empty"

    try:
        parsed_duration = int(duration)
        if parsed_duration < 1:
            return False, "Duration must be greater than 0"
    except ValueError:
        return False, "Duration must be a valid number"

    try:
        parsed_startDateTime = parse_datetime(startDateTime)
        if parsed_startDateTime is None:
            return (
                False,
                "StartDateTime must be a valid datetime in the format 'yyyy-MM-ddTHH\:mm\:ss' (2008-09-22T13:57:31)",
            )
    except ValueError:
        return (
            False,
            "StartDateTime must be a valid datetime in the format 'yyyy-MM-ddTHH\:mm\:ss' (2008-09-22T13:57:31)",
        )

    return True, None


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


@require_http_methods(["GET", "POST"])
def tickets(request, concertId):
    if request.method == "GET":
        return get_ticket(request, concertId)
    elif request.method == "POST":
        return buy_ticket(request, concertId)


@require_http_methods(["POST"])
def create_concert(request):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        user = User.objects.get(username=request.user.username)
        artist = Artist.objects.get(userId=user)

        request_concert = json.loads(request.body)
        displayname = request_concert["displayname"]
        description = request_concert["description"]

        concert_valid, validation_error = validate_concert(
            displayname,
            description,
            request_concert["duration"],
            request_concert["startDateTime"],
        )
        if not concert_valid:
            return JsonResponse({"message": validation_error}, status=400)

        duration = int(request_concert["duration"])
        startDateTime = parse_datetime(request_concert["startDateTime"])

        Concert.objects.create(
            displayname=displayname,
            description=description,
            duration=duration,
            startDateTime=startDateTime,
            artist=artist,
        )

        return JsonResponse({"message": "Successfully created concert"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Artist.DoesNotExist:
        return JsonResponse(
            {"message": "Unauthorized, you are not an artist"}, status=401
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["GET"])
def read_concert(request, concertId):
    try:
        concert = Concert.objects.values(
            "id",
            "displayname",
            "description",
            "artworkUrl",
            "duration",
            "startDateTime",
            artistId=F("artist"),
            artistDisplayname=F("artist__displayname"),
            artistAvatar=F("artist__avatarUrl"),
        ).get(pk=concertId)

        return JsonResponse(concert, safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse(
            {"message": "The specified concert does not exist"}, status=404
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["GET"])
def by_artist(request, artistId):
    try:
        artist = Artist.objects.get(pk=artistId)
        concert = Concert.objects.values(
            "id",
            "displayname",
            "description",
            "artworkUrl",
            "duration",
            "startDateTime",
            artistId=F("artist"),
            artistDisplayname=F("artist__displayname"),
            artistAvatar=F("artist__avatarUrl"),
        ).filter(artist=artist)

        return JsonResponse(list(concert), safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Artist.DoesNotExist:
        return JsonResponse(
            {"message": "The specified artist does not exist"}, status=404
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["PUT"])
def update_concert(request, concertId):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        user = User.objects.get(username=request.user.username)
        artist = Artist.objects.get(userId=user)

        request_concert = json.loads(request.body)
        displayname = request_concert["displayname"]
        description = request_concert["description"]

        concert_valid, validation_error = validate_concert(
            displayname,
            description,
            request_concert["duration"],
            request_concert["startDateTime"],
        )
        if not concert_valid:
            return JsonResponse({"message": validation_error}, status=400)

        duration = int(request_concert["duration"])
        startDateTime = parse_datetime(request_concert["startDateTime"])

        concert = Concert.objects.get(pk=concertId)
        if not concert.artist.id == artist.id:
            return JsonResponse(
                {"message": "Unauthorized, this concert does not belong to you"},
                status=401,
            )

        concert.displayname = displayname
        concert.description = description
        concert.duration = duration
        concert.startDateTime = startDateTime
        concert.save()

        return JsonResponse({"message": "Successfully updated concert"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse(
            {"message": "The specified concert does not exist"}, status=404
        )
    except Artist.DoesNotExist:
        return JsonResponse(
            {"message": "Unauthorized, you are not an artist"}, status=401
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["GET"])
def read_all(request):
    try:
        concerts = Concert.objects.values(
            "id",
            "displayname",
            "description",
            "artworkUrl",
            "duration",
            "startDateTime",
            artistId=F("artist"),
            artistDisplayname=F("artist__displayname"),
            artistAvatar=F("artist__avatarUrl"),
        ).all()

        return JsonResponse(list(concerts), safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["GET"])
def suggestions(request):
    try:

        suggestions_count = int(request.GET.get("count", 5))
        all_concerts = Concert.objects.values(
            "id",
            "displayname",
            "description",
            "artworkUrl",
            "duration",
            "startDateTime",
            artistId=F("artist"),
            artistDisplayname=F("artist__displayname"),
            artistAvatar=F("artist__avatarUrl"),
        ).all()

        concerts_count = Concert.objects.count()
        if suggestions_count > concerts_count:
            suggestions_count = concerts_count

        random_items = random.sample(list(all_concerts), suggestions_count)

        return JsonResponse(random_items, safe=False)
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["POST"])
def set_artwork(request, concertId):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        user = User.objects.get(username=request.user.username)
        artist = Artist.objects.get(userId=user)

        concert = Concert.objects.get(pk=concertId)
        if not concert.artist.id == artist.id:
            return JsonResponse(
                {"message": "Unauthorized, this concert does not belong to you"},
                status=401,
            )

        concert.artwork = request.FILES["artwork"]
        concert.artwork.name = "%s%s" % (uuid.uuid4(), concert.artwork.name)
        concert.save()

        concert.artworkUrl = concert.artwork.url
        concert.save()

        return JsonResponse({"message": "Successfully updated concert artwork"})
    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse(
            {"message": "The specified concert does not exist"}, status=404
        )
    except Artist.DoesNotExist:
        return JsonResponse(
            {"message": "Unauthorized, you are not an artist"}, status=401
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["POST"])
def buy_ticket(request, concertId):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        request_data = json.loads(request.body)
        send_confirmation_email = request_data["sendConfirmationEmail"]

        user = User.objects.get(username=request.user.username)
        concert = Concert.objects.get(pk=concertId)

        if concert.artist.userId.id == user.id:
            return JsonResponse(
                {"message": "Cannot buy a ticket for your own concert"}, status=400
            )

        existing_order_count = PurchaseOrder.objects.filter(
            Q(user=user) & Q(concert=concert)
        ).count()
        if existing_order_count > 0:
            return JsonResponse(
                {"message": "A purchase order for that concert is already existent"},
                status=409,
            )

        PurchaseOrder.objects.create(
            user=user, concert=concert, purchaseDateTime=datetime.datetime.now()
        )

        if send_confirmation_email == True:
            try:
                send_mail(
                    "Stagify - Purchase Confirmation",
                    "Hello there!\nWe confirm your ticket purchase for the concert '"
                    + concert.displayname
                    + "' which will take part on "
                    + concert.startDateTime.strftime("%m/%d/%Y, %H:%M:%S"),
                    "purchases@stagify.io",
                    [user.email],
                    fail_silently=False,
                )
            except Exception as e:
                return JsonResponse(
                    {
                        "message": "An unexpected error happened while sending the confirmation email"
                        + str(e)
                    },
                    status=500,
                )

        return JsonResponse(
            {"message": "Successfully created purchase order"}, status=200
        )

    except KeyError:
        return JsonResponse({"message": "Malformed data!"}, status=400)
    except Concert.DoesNotExist:
        return JsonResponse(
            {"message": "The specified concert does not exist"}, status=404
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


@require_http_methods(["GET"])
def get_ticket(request, concertId):
    try:
        if not request.user.is_authenticated:
            return JsonResponse({"message": "Unauthorized"}, status=401)

        user = User.objects.get(username=request.user.username)
        concert = Concert.objects.get(pk=concertId)

        existing_order_count = PurchaseOrder.objects.filter(
            Q(user=user) & Q(concert=concert)
        ).count()

        return JsonResponse({"ticketCount": existing_order_count}, status=200)

    except Concert.DoesNotExist:
        return JsonResponse(
            {"message": "The specified concert does not exist"}, status=404
        )
    except Exception as e:
        return JsonResponse(
            {"message": "An unexpected error happened: " + str(e)}, status=500
        )


urlpatterns = [
    path("concerts/", index, name="index endpoint - create new concert or list all"),
    path("concerts/suggestions", suggestions, name="concert suggestions for user"),
    path("concerts/<int:concertId>", concert_id, name="read or update concert"),
    path("concerts/artist/<int:artistId>", by_artist, name="read concerts by artist"),
    path("concerts/<int:concertId>/artwork", set_artwork, name="set concert artwork"),
    path(
        "concerts/<int:concertId>/tickets/",
        tickets,
        name="buy ticket or get ticket state for concert",
    ),
]
