from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()
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


class Categories(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=200)
    slug = models.SlugField(verbose_name='Идентификатор', unique=True)

    def __str__(self):
        return {self.name}


class Genres(models.Model):
    name = models.CharField(verbose_name='Жанр', max_length=200)
    slug = models.SlugField(verbose_name='Идентификатор', unique=True)

    def __str__(self):
        return {self.name}


class Titles(models.Model):
    name = models.CharField(verbose_name='Название', max_length=200)
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(
        Categories,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        blank=True, null=True,
        help_text='Выберите категорию'
    )
    genre = models.ForeignKey(
        Genres,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Жанр',
        blank=True, null=True,
        help_text='Выберите жанр'
    )
    year = models.DateTimeField(
        verbose_name='Год'
    )

    def __str__(self):
        return {self.name}