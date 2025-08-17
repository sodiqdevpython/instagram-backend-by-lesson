from django.db import models
from utils.models import BaseModel
from django.contrib.auth.models import AbstractUser
from . import choices
from uuid import uuid4
from rest_framework_simplejwt.tokens import RefreshToken

nb = dict(null=True, blank=True)

class User(BaseModel, AbstractUser):
    phone_number = models.CharField(max_length=9, unique=True, **nb)
    gender = models.CharField(max_length=6, choices=choices.GenderChoices.choices, **nb)
    bio = models.TextField(**nb)
    auth_type = models.CharField(max_length=12, choices=choices.AuthTypeChoices.choices)
    auth_status = models.CharField(max_length=13, choices=choices.AuthStatusChoices.choices, default=choices.AuthStatusChoices.NEW)
    image = models.ImageField(upload_to='users', **nb)

    def __str__(self):
        return self.username

    def create_temp_username(self):
        if not self.username:
            self.username = self.id

    def create_temp_password(self):
        if not self.password:
            self.password = str(uuid4())

    def hash_password(self):
        if not self.password.startswith('pbkdf2_sha256'):
            self.set_password(self.password)

    def clean(self):
        self.create_temp_username()
        self.create_temp_password()
        self.hash_password()

    def save(self, *args, **kwargs):
        self.clean()
        super(User, self).save(*args, **kwargs)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

class UserConfirm(BaseModel):
    code = models.CharField(max_length=4)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_confirm')
    expiration_time = models.DateTimeField()

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Tasdiqlash"
        verbose_name_plural = "Tasdiqlashlar"
        ordering = ['-created_at']