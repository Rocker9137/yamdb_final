from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


USER = "user"
ADMIN = "admin"
MODERATOR = "moderator"

ROLES = (
    ('user', 'user'),
    ('moderator', 'moderator'),
    ('admin', 'admin'),
)


class User(AbstractUser):
    """Создает модель пользователя."""
    username = models.CharField(
        unique=True,
        max_length=settings.MAX_LENGTH,
        blank=False,
        verbose_name='username'
    )
    email = models.EmailField('Почта пользователя', unique=True)
    bio = models.TextField('Биография', blank=True)
    role = models.CharField(
        max_length=settings.MAX_LENGTH_ROLE, choices=ROLES, default=USER
    )

    class Meta:
        verbose_name = 'Пользователь'
        ordering = ['id']

    @property
    def is_admin(self):
        return self.is_superuser or self.role == ADMIN

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    @property
    def is_user(self):
        return self.role == USER
