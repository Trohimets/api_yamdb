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

    @property
    def is_admin(self):
        return self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER


class Category(models.Model):
    name = models.CharField(
        verbose_name='Категория',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True
    )

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(
        verbose_name='Жанр',
        max_length=200
    )
    slug = models.SlugField(
        verbose_name='Идентификатор',
        unique=True
    )

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=200
    )
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        verbose_name='Категория',
        blank=True, null=True,
        help_text='Выберите категорию'
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name='Жанр',
        help_text='Выберите жанр'
    )
    year = models.IntegerField(
        verbose_name='Год'
    )

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
        help_text='Автор отзыва'
    )
    text = models.TextField(
        'Текст отзыва',
        help_text='Введите текст отзыва'
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Произведение',
        related_name='reviews',
        help_text='Произведение на которое написан отзыв'
    )
    pub_date = models.DateTimeField(
        'Дата публикации отзыва',
        auto_now_add=True,
        db_index=True,
        help_text='Дата публикации отзыва'
    )
    score = models.IntegerField(
        'Оценка',
        help_text='Введдите оценку'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='only_one_review'
            )
        ]


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
        help_text='Автор комментария'
    )
    text = models.TextField(
        'Текст комментария',
        help_text='Введите текст комментария'
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Отзыв',
        related_name='comments',
        help_text='Отзыв, к которому написан комментарий'
    )
    pub_date = models.DateTimeField(
        'Дата публикации комментария',
        db_index=True,
        auto_now_add=True,
        help_text='Дата публикации комментария'
    )
