# boards/models.py

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class Board(models.Model):
    name = models.CharField(_("Board Name"), max_length=120)
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
        related_name="memberships",
        null=True,
        blank=True,
    )
    invited_email = models.EmailField(null=True, blank=True)  # ایمیل دعوت‌شده (برای invites)
    board = models.ForeignKey(
        "boards.Board",
        on_delete=models.CASCADE,
        related_name="memberships"
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="member")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    class Meta:
        unique_together = ("user", "board")

    def __str__(self):
        if self.user:
            who = str(self.user)
        else:
            who = f"invited:{self.invited_email}"
        return f"{who} in {self.board} ({self.role}/{self.status})"

    def clean(self):

        if self.board and (not self.pk):
            accepted_count = BoardMembership.objects.filter(board=self.board, status="accepted").count()
            if self.status == "accepted" and accepted_count >= 10:
                raise ValidationError(_("This board already has maximum number of members (10)."))

        if self.user and (not self.pk):
            user_memberships_count = BoardMembership.objects.filter(user=self.user).exclude(status="rejected").count()
            if user_memberships_count >= 15:
                raise ValidationError(_("You have reached the maximum number of board memberships (15)."))

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
