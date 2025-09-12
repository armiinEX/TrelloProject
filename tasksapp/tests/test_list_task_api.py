# tasksapp/tests/test_list_task_api.py
from rest_framework.test import APIClient
from django.test import TestCase
from django.contrib.auth import get_user_model
from boards.models import Board, BoardMembership
from tasksapp.models import List, Task

class ListTaskApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user("u2", "u2@test.com", "pass123")
        self.client.force_authenticate(self.user)
        self.board = Board.objects.create(name="B1", owner=self.user)
        BoardMembership.objects.create(board=self.board, user=self.user, role="owner")
        self.list = List.objects.create(board=self.board, title="L1", order=1)

    def test_create_task(self):
        res = self.client.post("/api/tasks/", {"list": self.list.id, "title": "T1"})
        self.assertEqual(res.status_code, 201)
        self.assertEqual(Task.objects.count(), 1)
