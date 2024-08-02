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
    recommend_count = models.IntegerField()
    decommend_count = models.IntegerField()
    parent_id = models.IntegerField(null=True, blank=True)
    date = models.DateTimeField()


class Recommend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    recommend = models.BooleanField()
