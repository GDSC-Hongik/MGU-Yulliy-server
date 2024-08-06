from django.db import models
from accounts.models import User
from restaurants.models import Restaurant

# Create your models here.


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="reviews"
    )
    content = models.CharField(max_length=255)
    recommend_count = models.IntegerField(default=0)
    decommend_count = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)


class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="replies")
    content = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)


class Recommend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    recommend = models.BooleanField()
