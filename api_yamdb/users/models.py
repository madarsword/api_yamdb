from django.contrib.auth.models import AbstractUser
from django.db import models

from .validators import UsernameValidator


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'

    ROLE = (
          (USER, USER),
          (MODERATOR, MODERATOR),
          (ADMIN, ADMIN),
    )

    username_validator = UsernameValidator()
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
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
    confirmation_code = models.CharField(
        max_length=6,
        null=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_moderator(self):
        return self.role == "moderator"

    @property
    def is_user(self):
        return self.role == "user"
    
    def __str__(self):
        return self.username
