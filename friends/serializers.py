from rest_framework import serializers
from .models import Friend
from restaurants.models import Restaurant


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "google_rating",
            "naver_rating",
            "kakao_rating",
            "address",
            "latitude",
            "longitude",
        ]
