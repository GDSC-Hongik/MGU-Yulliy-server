from rest_framework import serializers
from .models import Friend
from restaurants.models import Restaurant, UserRestaurantsList
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "name", "profile_img", "reliability"]


class FriendRequestSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    common_restaurant_count = serializers.SerializerMethodField()

    class Meta:
        model = Friend
        fields = ["user", "state", "common_restaurant_count"]

    def get_common_restaurant_count(self, obj):
        try:
            user = obj.user
            # friend_user = self.context.get('request').user
            friend_user = User.objects.get(id=21)

            user_restaurants = set(
                UserRestaurantsList.objects.filter(user=user).values_list(
                    "restaurant_id", flat=True
                )
            )
            friend_restaurants = set(
                UserRestaurantsList.objects.filter(user=friend_user).values_list(
                    "restaurant_id", flat=True
                )
            )
            return len(user_restaurants.intersection(friend_restaurants))
        except User.DoesNotExist:
            return 0


class FriendRecommendSerializer(serializers.ModelSerializer):
    common_restaurant_count = serializers.SerializerMethodField()
    common_restaurants = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "name",
            "profile_img",
            "reliability",
            "common_restaurant_count",
            "common_restaurants",
        ]

    def get_common_restaurant_count(self, obj):
        user = self.context.get("user")
        user_restaurants = set(
            UserRestaurantsList.objects.filter(user=user).values_list(
                "restaurant_id", flat=True
            )
        )
        friend_restaurants = set(
            UserRestaurantsList.objects.filter(user=obj).values_list(
                "restaurant_id", flat=True
            )
        )
        return len(user_restaurants.intersection(friend_restaurants))

    def get_common_restaurants(self, obj):
        user = self.context.get("user")
        user_restaurants = set(
            UserRestaurantsList.objects.filter(user=user).values_list(
                "restaurant_id", flat=True
            )
        )
        friend_restaurants = UserRestaurantsList.objects.filter(
            user=obj, restaurant_id__in=user_restaurants
        ).values("restaurant__name", "restaurant__image_url")[:2]
        return friend_restaurants


class FriendSerializer(serializers.ModelSerializer):
    friend = UserSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ["friend", "state"]


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


class RestaurantSerializer(serializers.ModelSerializer):
    # reviews = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"


class FriendRestaurantSerializer(serializers.ModelSerializer):
    restaurant = RestaurantlistSerializer()

    class Meta:
        model = UserRestaurantsList
        fields = "__all__"
