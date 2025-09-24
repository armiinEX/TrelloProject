from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from boards.models import Board, BoardMembership
from tasksapp.models import List, Task

User = get_user_model()

class TaskApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user("o", "o@test.com", "pass123")
        self.client.force_authenticate(self.owner)
        self.board = Board.objects.create(name="B1", owner=self.owner)
        BoardMembership.objects.create(board=self.board, user=self.owner, role="owner", status="accepted")
        self.list = List.objects.create(board=self.board, title="L1", order=1)

    def test_create_task_on_list(self):
        res = self.client.post(f"/api/lists/{self.list.id}/tasks/", {"title":"T1"}, format="json")
        self.assertEqual(res.status_code, 201)
        self.assertTrue(Task.objects.filter(list=self.list, title="T1").exists())