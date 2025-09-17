# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class User(AbstractUser):
    preferred_language = models.CharField(
        max_length=5,
        choices=[("en", _("English")), ("fa", _("Farsi"))],
        default="en",
        verbose_name=_("Preferred Language"),
        help_text=_("Preferred language for the user interface"),
    )

    def __str__(self):
        return self.username
