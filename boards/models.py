# boards/models.py
from django.db import models
from django.conf import settings

class Board(models.Model):
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=20, default="#4f46e5")  # indigo-ish
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_boards")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class BoardMembership(models.Model):
    ROLE_CHOICES = [("owner","Owner"),("member","Member")]
    STATUS_CHOICES = [("accepted","Accepted")]  # دعوت‌نامه‌ها بعداً
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="memberships")
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="memberships")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="accepted")

    class Meta:
        unique_together = ("user","board")

    def __str__(self):
        return f"{self.user} in {self.board} ({self.role})"
