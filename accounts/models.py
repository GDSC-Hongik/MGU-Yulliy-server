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

    profile_img = models.ImageField(
        default="default_profile_img.jpg", upload_to="profile_imgs"
    )

    reliability = models.SmallIntegerField(default=80)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "username"]

    def __str__(self):
        return self.name
