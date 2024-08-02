from rest_framework import serializers
from .models import Friend
from restaurants.models import Restaurant, UserRestaurantsList


class FriendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Friend
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):
    # reviews = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"


class RestaurantSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = UserRestaurantsList
        fields = "__all__"
