from django.contrib.auth.models import AbstractUser
from django.db import models

USER = "user"
MODERATOR = "moderator"
ADMIN = "admin"
ROLES = [
    ("user", USER),
    ("moderator", MODERATOR),
    ("admin", ADMIN)
]

class User(AbstractUser):
    bio = models.TextField(
        blank=True,
    )
    role = models.CharField(
        max_length=100,
        choices=ROLES,
        default=USER
    )
    