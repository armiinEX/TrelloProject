# boards/tests/test_invitations.py
from django.test import TestCase
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from boards.models import Board, BoardMembership

User = get_user_model()

class InvitationsTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.owner = User.objects.create_user("owner", "owner@test.com", "pass123")
        self.invitee_email = "invited@test.com"
        self.board = Board.objects.create(name="B1", owner=self.owner)
        BoardMembership.objects.create(board=self.board, user=self.owner, role="owner", status="accepted")
        self.client.force_authenticate(self.owner)

    def test_invite_by_email_creates_membership(self):
        res = self.client.post(f"/api/boards/{self.board.id}/invite/", {"email": self.invitee_email}, format="json")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(BoardMembership.objects.filter(board=self.board, invited_email=self.invitee_email).exists())