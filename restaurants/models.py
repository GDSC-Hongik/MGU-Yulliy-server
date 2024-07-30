from django.db import models
from users.models import User

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
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)


class UserRestaurantList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "restaurant")
