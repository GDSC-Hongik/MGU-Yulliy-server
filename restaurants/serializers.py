from rest_framework import serializers
from .models import Restaurant, SearchHistory, UserRestaurantsList

# from reviews.serializers import ReviewSerializer


class RestaurantSerializer(serializers.ModelSerializer):
    # reviews = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"


"""
    def get_reviews(self, obj):
        reviews = obj.reviews.order_by("-recommend_count")[:4]
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
"""


class RestaurantListSerializer(serializers.ModelSerializer):
    rating_average = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = [
            "id",
            "name",
            "google_rating",
            "naver_rating",
            "kakao_rating",
            "address",
        ]

    def get_rating_average(self, obj):
        return obj.rating_average


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ["query", "timestamp"]


class UserRestaurantListSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()

    class Meta:
        model = UserRestaurantsList
        fields = "__all__"
