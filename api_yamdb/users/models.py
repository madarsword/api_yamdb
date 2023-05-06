from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import validate_username


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE = (
        (USER, USER),
        (MODERATOR, MODERATOR),
        (ADMIN, ADMIN),
    )

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=(validate_username,)
    )
    email = models.EmailField(max_length=254, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    bio = models.TextField(blank=True)
    role = models.CharField(
        max_length=9,
        choices=ROLE,
        default=USER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['last_name']

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_user(self):
        return self.role == self.USER
