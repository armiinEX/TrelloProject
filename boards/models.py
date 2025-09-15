# boards/models.py

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Board(models.Model):
    name = models.CharField(max_length=120)
    color = models.CharField(max_length=20, default="#4f46e5")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="owned_boards"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def clean(self):
        if Board.objects.filter(owner=self.owner).count() >= 5 and not self.pk:
            raise ValidationError(
                _("You have reached the maximum number of boards (5).")
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)


class BoardMembership(models.Model):
    ROLE_CHOICES = [("owner", "Owner"), ("member", "Member")]
    STATUS_CHOICES = [
    ("pending", "Pending"),
    ("accepted", "Accepted"),
    ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    board = models.ForeignKey(
        Board,
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    class Meta:
        unique_together = ("user", "board")

    def __str__(self):
        return f"{self.user} in {self.board} ({self.role})"

    def clean(self):
        if BoardMembership.objects.filter(board=self.board).count() >= 10 and not self.pk:
            raise ValidationError(
                _("This board already has maximum number of members (10).")
            )
        if BoardMembership.objects.filter(user=self.user).count() >= 15 and not self.pk:
            raise ValidationError(
                _("You have reached the maximum number of board memberships (15).")
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
