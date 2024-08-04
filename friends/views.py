# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# from django.contrib.auth.decorators import login_required
from restaurants.models import UserRestaurantsList, Restaurant
from .serializers import (
    FriendSerializer,
    FriendRequestSerializer,
    RestaurantlistSerializer,
    FriendRecommendSerializer,
)
from accounts.models import User
from .models import Friend, FriendRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
import random


@api_view(["GET"])
# @login_required
def friend_restaurant_list(request, id):
    try:
        # id에 해당하는 친구를 가져옴
        friend = User.objects.get(id=id)

        # 친구의 맛집 리스트를 가져옴
        friend_restaurants = UserRestaurantsList.objects.filter(user=friend)
        restaurant_ids = friend_restaurants.values_list("restaurant_id", flat=True)
        restaurants = Restaurant.objects.filter(id__in=restaurant_ids)

        serializer = RestaurantlistSerializer(restaurants, many=True)

        return Response({"results": serializer.data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {"message": "Friend not found"}, status=status.HTTP_404_NOT_FOUND
        )


@csrf_exempt
@api_view(["GET"])
# @login_required
def friend_list(request):
    try:
        # user = request.user
        user = User.objects.get(id=21)

        friend_request = FriendRequest.objects.filter(to_user=user, state="pending")
        friend_request_serialized = FriendRequestSerializer(
            friend_request, context={"request": request}, many=True
        ).data

        friends = Friend.objects.filter(user=user)
        friends_serialized = FriendSerializer(friends, many=True).data

        user_restaurants = set(
            UserRestaurantsList.objects.filter(user=user).values_list(
                "restaurant_id", flat=True
            )
        )
        potential_friends = (
            User.objects.exclude(id=user.id)
            .annotate(
                common_restaurant_count=Count(
                    "userrestaurantslist__restaurant_id",
                    filter=Q(userrestaurantslist__restaurant_id__in=user_restaurants),
                )
            )
            .order_by("-common_restaurant_count")[:7]
        )

        friend_recommend_serialized = FriendRecommendSerializer(
            potential_friends,
            many=True,
            context={"request": request, "user": user, "include_restaurants": False},
        ).data

        data = {
            "friend_request": friend_request_serialized,
            "friends": friends_serialized,
            "friend_recommend": friend_recommend_serialized,
        }

        return Response(data)

    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@csrf_exempt
@api_view(["GET"])
# @login_required
def friend_recommend(request):
    try:
        # user = request.user
        user = User.objects.get(id=21)

        user_restaurants = set(
            UserRestaurantsList.objects.filter(user=user).values_list(
                "restaurant_id", flat=True
            )
        )
        potential_friends = (
            User.objects.exclude(id=user.id)
            .annotate(
                common_restaurant_count=Count(
                    "userrestaurantslist__restaurant_id",
                    filter=Q(userrestaurantslist__restaurant_id__in=user_restaurants),
                )
            )
            .order_by("-common_restaurant_count")[:7]
        )

        if potential_friends:
            random_friend = random.choice(potential_friends)
            friend_recommend_serialized = FriendRecommendSerializer(
                random_friend,
                context={"request": request, "user": user, "include_restaurants": True},
            ).data
            return Response(friend_recommend_serialized)

        return Response(
            {"message": "No recommended friends found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
