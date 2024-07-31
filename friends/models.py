from django.db import models
from accounts.models import User

# Create your models here.


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_of")
    state = models.CharField(max_length=20, null=True, blank=True)
