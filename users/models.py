from django.contrib.auth.models import AbstractUser
from django.db import models

from catalog.models import NULLABLE


class User(AbstractUser):
    username = None
    email = models.EmailField(max_length=255, unique=True)

    avatar = models.ImageField(upload_to='avatars', **NULLABLE, verbose_name='Аватар')
    phone = models.CharField(max_length=255, **NULLABLE, verbose_name='Телефон')
    country = models.CharField(max_length=255, **NULLABLE, verbose_name='Страна')

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
