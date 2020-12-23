from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Artist
import json

class ArtistTest(TestCase):
    def setUp(self):
        super_user = User.objects.create_superuser(username="superuser", password="superuser")
        normal_user1 = User.objects.create_user(username="normaluser", password="normaluser")
        normal_user2 = User.objects.create_user(username="normaluser2", password="normaluser2")

        Artist.objects.create(displayname="Displayname #1",description="Description #1", userId=normal_user1)
        Artist.objects.create(displayname="Displayname #2",description="Description #2 test", userId=normal_user2)


    def test_create_artist_with_normal_user_returns_401_unauthorized(self):
        login = self.client.login(username='normaluser', password='normaluser')
        payload = json.loads('{"displayname": "lala"}')

        response = self.client.post("/api/artists/", payload, content_type="application/json")

        response_object = json.loads(response.content)

        self.assertTrue(login)
        self.assertEqual(response_object["message"], "Unauthorized")
        self.assertEqual(response.status_code, 401)

    def test_create_artist_with_no_user_returns_401_unauthorized(self):
        payload = json.loads('{"displayname": "lala"}')

        response = self.client.post("/api/artists/", payload, content_type="application/json")

        response_object = json.loads(response.content)

        self.assertEqual(response_object["message"], "Unauthorized")
        self.assertEqual(response.status_code, 401)

    def test_create_artist_with_super_user_and_non_existent_user_returns_404_no_user(self):
        login = self.client.login(username='superuser', password='superuser')
        payload = json.loads('{"displayname": "lala", "description": "lala", "userId": 5}')

        response = self.client.post("/api/artists/", payload, content_type="application/json")

        response_object = json.loads(response.content)

        self.assertTrue(login)
        self.assertEqual(response_object["message"], "The specified user does not exist")
        self.assertEqual(response.status_code, 404)

    def test_create_artist_with_super_user_and_missing_data_returns_400_malformed_data(self):
        login = self.client.login(username='superuser', password='superuser')
        payload = json.loads('{"displayname": "Justin 3"}')

        response = self.client.post("/api/artists/", payload, content_type="application/json")

        response_object = json.loads(response.content)

        self.assertTrue(login)
        self.assertEqual(response_object["message"], "Malformed data!")
        self.assertEqual(response.status_code, 400)

    def test_search_artist_returns_correct_artist_and_200_ok(self):
        response = self.client.get("/api/artists/search/test")

        response_object = json.loads(response.content)

        self.assertEqual(len(response_object), 1)
        self.assertEqual(response_object[0]["id"], 2)
        self.assertEqual(response_object[0]["displayname"], "Displayname #2")
        self.assertEqual(response.status_code, 200)

    def test_read_all_artists_returns_all_artists_and_200_ok(self):
        response = self.client.get("/api/artists/")

        response_object = json.loads(response.content)

        self.assertEqual(len(response_object), 2)
        self.assertEqual(response_object[0]["id"], 1)
        self.assertEqual(response_object[1]["id"], 2)
        self.assertEqual(response.status_code, 200)

    def test_read_specific_artist_returns_correct_artist_and_200_ok(self):
        response = self.client.get("/api/artists/1")

        response_object = json.loads(response.content)

        self.assertEqual(response_object["id"], 1)
        self.assertEqual(response.status_code, 200)

    def test_read_specific_non_existent_artist_returns_404_not_found(self):
        response = self.client.get("/api/artists/100")

        response_object = json.loads(response.content)

        self.assertEqual(response_object["message"], "The specified artist does not exist")
        self.assertEqual(response.status_code, 404)

    def test_update_artist_without_being_artist_returns_401_not_an_artist(self):
        login = self.client.login(username='superuser', password='superuser')
        payload = json.loads('{"displayname": "lala", "description": "lala", "userId": 5}')

        response = self.client.put("/api/artists/", payload, content_type="application/json")

        response_object = json.loads(response.content)

        self.assertTrue(login)
        self.assertEqual(response_object["message"], "Unauthorized, you are not an artist")
        self.assertEqual(response.status_code, 401)

    def test_update_artist_with_being_artist_changes_values_and_returns_200_ok(self):
        login = self.client.login(username='normaluser', password='normaluser')
        payload = json.loads('{"displayname": "lala 1", "description": "lala 2"}')

        response = self.client.put("/api/artists/", payload, content_type="application/json")

        response_object = json.loads(response.content)
        updated_artist = Artist.objects.get(pk=1)

        self.assertTrue(login)
        self.assertEqual(response_object["message"], "Successfully updated artist")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_artist.displayname, "lala 1")
        self.assertEqual(updated_artist.description, "lala 2")