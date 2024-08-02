# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# from django.contrib.auth.decorators import login_required
from restaurants.models import UserRestaurantsList
from .serializers import RestaurantSerializer, FriendSerializer
from accounts.models import User
from .models import Friend
from django.views.decorators.csrf import csrf_exempt


@api_view(["GET"])
# @login_required
def friend_restaurant_list(request, id):
    try:
        # id에 해당하는 친구를 가져옴
        friend = User.objects.get(id=id)

        # 친구의 맛집 리스트를 가져옴
        friend_restaurants = UserRestaurantsList.objects.filter(user=friend)
        serializer = RestaurantSerializer(friend_restaurants, many=True)

        return Response({"restaurants": serializer.data}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {"message": "Friend not found"}, status=status.HTTP_404_NOT_FOUND
        )


@csrf_exempt
@api_view(["GET"])
# @login_required
def friend_list(request):
    user = User.objects.get(id=21)

    friend_request = Friend.objects.filter(friend=user, state="request")
    friend_request_serialized = FriendSerializer(friend_request, many=True).data

    friend_approve = Friend.objects.filter(user=user, state="approve")
    friend_approve_serialized = FriendSerializer(friend_approve, many=True).data

    data = {
        "friend_request": friend_request_serialized,
        "friends": friend_approve_serialized,
    }

    return Response(data)
