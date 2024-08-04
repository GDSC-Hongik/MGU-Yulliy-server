from rest_framework import serializers
from .models import Restaurant, SearchHistory, UserRestaurantsList

from reviews.serializers import ReviewSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    rating_average = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_rating_average(self, obj):
        return obj.rating_average()


class RestaurantListSerializer(serializers.ModelSerializer):
    rating_average = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "food_type",
            "rating_average",
            "address",
        ]

    def get_rating_average(self, obj):
        return obj.rating_average()


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ["id", "query", "timestamp"]


class RestaurantlistSerializer(serializers.ModelSerializer):
    rating_average = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "food_type",
            "rating_average",
            "latitude",
            "longitude",
            "image_url",
        ]

    def get_rating_average(self, obj):
        return obj.rating_average()


class UserRestaurantListSerializer(serializers.ModelSerializer):
    restaurant = RestaurantlistSerializer()

    class Meta:
        model = UserRestaurantsList
        fields = "__all__"


class RestaurantDetailSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField()
    rating_average = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_reviews(self, obj):
        reviews = obj.reviews.order_by("-recommend_count")[:4]
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data

    def get_rating_average(self, obj):
        return obj.rating_average()
