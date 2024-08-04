from django.db import models
from accounts.models import User

# Create your models here.


class Friend(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friends")
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name="friend_of")

    class Meta:
        unique_together = ("user", "friend")


class FriendRequest(models.Model):
    STATE_CHOICES = [
        ("pending", "Pending"),
        ("accepted", "Accepted"),
        ("declined", "Declined"),
    ]

    from_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="sent_friend_requests"
    )
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="received_friend_requests"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default="request")

    class Meta:
        unique_together = ("from_user", "to_user")
