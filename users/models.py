from django.db import models
from utils.models import BaseModel
from django.contrib.auth.models import AbstractUser
from . import choices

nb = dict(null=True, blank=True)

class User(BaseModel, AbstractUser):
    phone_number = models.CharField(max_length=9, unique=True)
    gender = models.CharField(max_length=6, choices=choices.GenderChoices.choices)
    bio = models.TextField(**nb)
    auth_type = models.CharField(max_length=12, choices=choices.AuthTypeChoices.choices)
    auth_status = models.CharField(max_length=13, choices=choices.AuthStatusChoices.choices)
    image = models.ImageField(upload_to='users', **nb)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"