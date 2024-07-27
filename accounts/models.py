from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)

    name = models.CharField(
        max_length=20,
        unique=True,
        null=False,
        error_messages={"unique": "이미 사용 중인 닉네임입니다."},
    )

    profile_pic = models.ImageField(
        default="default_profile_pic.jpg", upload_to="profile_pics"
    )

    reliability = models.IntegerField(default=100)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name
