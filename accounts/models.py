from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
# Create your models here.


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = []

    objects = UserManager()

    USERNAME_FIELD = 'email'
