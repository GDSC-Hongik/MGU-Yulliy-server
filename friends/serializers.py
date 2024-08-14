from rest_framework import serializers
from .models import Friend, FriendRequest
from restaurants.models import Restaurant, UserRestaurantsList
from accounts.models import User


class UserSerializer(serializers.ModelSerializer):
    is_evaluated = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "name", "profile_img", "reliability", "is_evaluated"]

    def get_is_evaluated(self, obj):
        user = self.context["request"].user
        try:
            friend = Friend.objects.get(user=user, friend=obj)
            return friend.is_evaluated
        except Friend.DoesNotExist:
            return False


class FriendRequestSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="from_user.id")
    name = serializers.CharField(source="from_user.name")
    profile_img = serializers.URLField(source="from_user.profile_img.url")
    reliability = serializers.IntegerField(source="from_user.reliability")
    common_restaurant_count = serializers.SerializerMethodField()

    class Meta:
        model = FriendRequest
        fields = [
            "id",
            "name",
            "profile_img",
            "reliability",
            "common_restaurant_count",
        ]

    def get_common_restaurant_count(self, obj):
        try:
            user = obj.from_user
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
    profile_img = serializers.URLField(source="profile_img.url")

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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        include_restaurants = self.context.get("include_restaurants", False)
        if not include_restaurants:
            representation.pop("common_restaurants")
        return representation


class FriendSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source="friend.id")
    name = serializers.CharField(source="friend.name")
    profile_img = serializers.URLField(source="friend.profile_img.url")
    reliability = serializers.IntegerField(source="friend.reliability")

    class Meta:
        model = Friend
        fields = [
            "id",
            "name",
            "profile_img",
            "reliability",
        ]


class RestaurantlistSerializer(serializers.ModelSerializer):
    rating_average = serializers.SerializerMethodField()
    image_url = serializers.SerializerMethodField()

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
        return str(obj.rating_average())

    def get_image_url(self, obj):
        if obj.image_url:  # image_url이 null이 아닌 경우에만 처리
            base_url = "https://mugou.s3.ap-southeast-2.amazonaws.com/images/"
            image_name = f"{obj.name}.jpg"  # 식당 이름을 사용하여 이미지 파일명 생성
            return f"{base_url}{image_name}"
        else:
            return "https://mugou.s3.ap-southeast-2.amazonaws.com/images/default_profile_img.jpg"


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
