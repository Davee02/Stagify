from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Artist, Concert
from datetime import date
import json

class ConcertTest(TestCase):
    def setUp(self):
        artist_user = User.objects.create_user(username="artistuser", password="artistuser")
        normal_user = User.objects.create_user(username="normaluser", password="normaluser")

        for i in range(1, 10):
            i_str = str(i)

            artist = Artist.objects.create(displayname="Displayname #" + i_str, description="Description #" + i_str, userId=artist_user)
            Concert.objects.create(displayname="Displayname #" + i_str, description="Description #" + i_str,
                             duration=i, startDateTime=date.today(), artist=artist)

    def test_create_concert_with_no_user_returns_401_unauthorized(self):
        payload = json.loads('{"displayname": "lala"}')

        response = self.client.post("/api/concerts/", payload, content_type="application/json")
        response_object = json.loads(response.content)

        self.assertEqual(response_object["message"], "Unauthorized")
        self.assertEqual(response.status_code, 401)

    def test_update_concert_with_no_user_returns_401_unauthorized(self):
        payload = json.loads('{"displayname": "lala"}')

        response = self.client.put("/api/concerts/1", payload, content_type="application/json")
        response_object = json.loads(response.content)

        self.assertEqual(response_object["message"], "Unauthorized")
        self.assertEqual(response.status_code, 401)

    def test_get_suggestions_with_no_user_returns_401_unauthorized(self):
        response = self.client.get("/api/concerts/suggestions")
        response_object = json.loads(response.content)

        self.assertEqual(response_object["message"], "Unauthorized")
        self.assertEqual(response.status_code, 401)

    def test_set_artwork_with_no_user_returns_401_unauthorized(self):
        response = self.client.post("/api/concerts/1/artwork")
        response_object = json.loads(response.content)

        self.assertEqual(response_object["message"], "Unauthorized")
        self.assertEqual(response.status_code, 401)

    def test_create_concert_with_no_artist_user_returns_401_unauthorized(self):
        payload = json.loads('{"displayname": "lala"}')
        login = self.client.login(username='normaluser', password='normaluser')

        response = self.client.post("/api/concerts/", payload, content_type="application/json")
        response_object = json.loads(response.content)

        self.assertTrue(login)
        self.assertEqual(response_object["message"], "Unauthorized, you are not an artist")
        self.assertEqual(response.status_code, 401)

    def test_update_concert_with_no_artist_user_returns_401_unauthorized(self):
        payload = json.loads('{"displayname": "lala"}')
        login = self.client.login(username='normaluser', password='normaluser')

        response = self.client.put("/api/concerts/1", payload, content_type="application/json")
        response_object = json.loads(response.content)

        self.assertTrue(login)
        self.assertEqual(response_object["message"], "Unauthorized, you are not an artist")
        self.assertEqual(response.status_code, 401)

    def test_get_concert_by_artist_returns_concerts_and_200_ok(self):
        response = self.client.get("/api/concerts/artist/1")
        response_object = json.loads(response.content)

        self.assertEqual(len(response_object), 1)
        self.assertEqual(response_object[0]["id"], 1)
        self.assertEqual(response.status_code, 200)

    def test_get_all_concerts_returns_all_concerts_and_200_ok(self):
        response = self.client.get("/api/concerts/")
        response_object = json.loads(response.content)

        self.assertEqual(len(response_object), 9)
        self.assertEqual(response.status_code, 200)


    def test_get_suggestions_concerts_returns_5_concerts_and_200_ok(self):
        login = self.client.login(username='normaluser', password='normaluser')

        response = self.client.get("/api/concerts/suggestions")
        response_object = json.loads(response.content)

        self.assertTrue(login)
        self.assertEqual(len(response_object), 5)
        self.assertEqual(response.status_code, 200)

    def test_get_suggestions_with_custom_amount_concerts_returns_correct_amount_of_concerts_and_200_ok(self):
        login = self.client.login(username='normaluser', password='normaluser')

        response = self.client.get("/api/concerts/suggestions?count=7")
        response_object = json.loads(response.content)

        self.assertTrue(login)
        self.assertEqual(len(response_object), 7)
        self.assertEqual(response.status_code, 200)