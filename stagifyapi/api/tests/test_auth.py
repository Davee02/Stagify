from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Artist, Concert
from datetime import date
import json

class AuthTest(TestCase):
    def setUp(self):
        normal_user1 = User.objects.create_user(username="normaluser1", password="normaluser1")
        normal_user2 = User.objects.create_user(username="normaluser2", password="normaluser2")

    def test_register_with_duplicate_username_returns_409_conflict(self):
        payload = json.loads('{"username": "normaluser1", "email": "a@a.a", "password": "password", "firstname": "firstname", "lastname": "lastname"}')

        response = self.client.post("/api/user/register", payload, content_type="application/json")
        response_object = json.loads(response.content)

        self.assertEqual(response_object["message"], "An user with the same username already exists")
        self.assertEqual(response.status_code, 409)

    def test_update_with_duplicate_username_returns_409_conflict(self):
        login = self.client.login(username='normaluser1', password='normaluser1')
        payload = json.loads('{"username": "normaluser2", "email": "a@a.a", "password": "password", "firstname": "firstname", "lastname": "lastname"}')

        response = self.client.put("/api/user/", payload, content_type="application/json")
        response_object = json.loads(response.content)

        self.assertTrue(login)
        self.assertEqual(response_object["message"], "An user with the same username already exists")
        self.assertEqual(response.status_code, 409)