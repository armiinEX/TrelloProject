from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from boards.models import Board, BoardMembership
from tasksapp.models import List

User = get_user_model()

class ListsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user("o", "o@test.com", "pass123")
        self.client.force_authenticate(self.owner)
        self.board = Board.objects.create(name="B1", owner=self.owner)
        BoardMembership.objects.create(board=self.board, user=self.owner, role="owner", status="accepted")

    def test_create_list_on_board(self):
        res = self.client.post(f"/api/boards/{self.board.id}/lists/", {"title":"L1"}, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(List.objects.filter(board=self.board, title="L1").exists())