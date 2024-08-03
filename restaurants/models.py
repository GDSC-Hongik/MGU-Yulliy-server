from django.db import models
from accounts.models import User

# Create your models here.


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    food_type = models.CharField(max_length=20, null=True, blank=True)
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

    def rating_average(self):
        ratings = [self.rating_naver, self.rating_kakao, self.rating_google]
        valid_ratings = [rating for rating in ratings if rating is not None]
        if valid_ratings:
            return sum(valid_ratings) / len(valid_ratings)
        return 0


class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]


class UserRestaurantsList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "restaurant")
