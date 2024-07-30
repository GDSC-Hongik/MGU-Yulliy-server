from django.db import models

# Create your models here.


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    rating_naver = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    rating_kakao = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    rating_google = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True
    )
    address = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=11, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
