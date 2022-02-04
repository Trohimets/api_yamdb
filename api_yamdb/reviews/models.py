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
    email = models.EmailField(
        unique=True,
    )
    bio = models.TextField(
        blank=True,
    )
    role = models.CharField(
        max_length=100,
        choices=ROLES,
        default=USER
    )

    def admin(self):
        return self.role == 'admin'

    def moderator(self):
        return self.role == 'moderator'

    def user(self):
        return self.role == 'user'