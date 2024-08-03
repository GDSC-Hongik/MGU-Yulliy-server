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


class FriendSerializer(serializers.ModelSerializer):
    friend = UserSerializer(read_only=True)

    class Meta:
        model = Friend
        fields = ["friend", "state"]


class RestaurantlistSerializer(serializers.ModelSerializer):
    rating_average = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ["name", "food_type", "rating_average", "latitude", "longitude"]

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
