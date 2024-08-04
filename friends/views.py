# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.views import APIView

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

# from django.contrib.auth.decorators import login_required
from restaurants.models import UserRestaurantsList, Restaurant
from .serializers import (
    FriendSerializer,
    FriendRequestSerializer,
    RestaurantlistSerializer,
    FriendRecommendSerializer,
    RestaurantSerializer,
)

# from .serializers import FriendSerializer, FriendRequestSerializer
from accounts.models import User
from .models import Friend, FriendRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
import random

from django.shortcuts import get_object_or_404


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


# 친구신청
class FriendRequestView(APIView):
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        action = request.data.get("action")
        friend_id = request.data.get("friend_id")

        if action == "send":
            return self.send_request(request, friend_id)
        elif action == "accept":
            return self.accept_request(request, friend_id)
        elif action == "decline":
            return self.decline_request(request, friend_id)
        else:
            return Response(
                {"message": "올바르지 않은 요청입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

    # 친구 요청
    def send_request(self, request, friend_id):
        to_user = get_object_or_404(User, id=friend_id)
        from_user = request.user

        if FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            return Response(
                {"message": "이미 친구 요청을 보냈습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        friend_request = FriendRequest(
            from_user=from_user, to_user=to_user, state="pending"
        )
        friend_request.save()

        return Response({"message": "친구 요청을 보냈습니다."}, status=status.HTTP_201_CREATED)

    # 친구 수락
    def accept_request(self, request, friend_id):
        # 친구 요청을 보낸 사용자의 id와 일치하는 요청이 있는지 확인
        friend_request = get_object_or_404(FriendRequest, from_user__id=friend_id)

        if friend_request.to_user != request.user:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        if friend_request.state != "pending":
            return Response(
                {"message": "이미 처리된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        friend_request.state = "accepted"
        friend_request.save()

        # 양방향 친구 관계 설정
        from_user = friend_request.from_user
        to_user = friend_request.to_user

        friend_relation = Friend.objects.create(user=from_user, friend=to_user)
        friend_relation.save()
        reverse_friend_relation = Friend.objects.create(user=to_user, friend=from_user)
        reverse_friend_relation.save()

        return Response({"message": "친구 신청을 수락했습니다."}, status=status.HTTP_200_OK)

    # 친구 거절
    def decline_request(self, request, friend_id):
        friend_request = get_object_or_404(FriendRequest, from_user__id=friend_id)

        if friend_request.to_user != request.user:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_403_FORBIDDEN)
        if friend_request.state != "pending":
            return Response(
                {"message": "이미 처리된 요청입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        friend_request.state = "declined"
        friend_request.save()

        return Response({"message": "친구 신청을 거절했습니다."}, status=status.HTTP_200_OK)
