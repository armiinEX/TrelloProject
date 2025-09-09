# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    preferred_language = models.CharField(
        max_length=5, choices=[("en","English"),("fa","Farsi")], default="en"
    )

    def __str__(self):
        return self.username
