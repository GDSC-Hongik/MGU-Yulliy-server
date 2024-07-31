from django.db import models

# Create your models here.


class User(models.Model):
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    nickname = models.CharField(max_length=255, null=True, blank=True)
    image = models.CharField(max_length=255, null=True, blank=True)
    reliability = models.SmallIntegerField(null=True, blank=True)
