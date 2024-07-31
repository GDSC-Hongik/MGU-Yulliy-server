from rest_framework import serializers
from .models import Restaurant, SearchHistory, UserRestaurantList


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = "__all__"


class RestaurantListSerializer(serializers.ModelSerializer):
    rating_average = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ["name", "rating_average", "address"]

    def get_rating_average(self, obj):
        return obj.rating_average


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ["query", "timestamp"]


class UserRestaurantListSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = UserRestaurantList
        fields = "__all__"
