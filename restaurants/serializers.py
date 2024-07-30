from rest_framework import serializers
from .models import Restaurant, UserRestaurantList


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class UserRestaurantListSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = UserRestaurantList
        fields = "__all__"
