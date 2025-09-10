# boards/tests/test_board_api.py
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.test import TestCase
from boards.models import Board, BoardMembership

class BoardApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username="u1", password="pass123")
        self.client.force_authenticate(self.user)

    def test_create_board_sets_owner_and_membership(self):
        res = self.client.post("/api/boards/", {"name":"W1","color":"#000000"}, format="json")
        self.assertEqual(res.status_code, 201)
        b = Board.objects.get(id=res.data["id"])
        self.assertEqual(b.owner, self.user)
        self.assertTrue(BoardMembership.objects.filter(board=b, user=self.user, role="owner").exists())
