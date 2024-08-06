from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from restaurants.models import Restaurant
from .models import Review
from .serializers import ReviewSerializer, ReplySerializer

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated


@api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def review_write(request, pk):
    user = User.objects.get(id=21)

    try:
        restaurant = Restaurant.objects.get(pk=pk)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND
        )

    data = request.data
    data["user"] = user.id
    data["restaurant"] = restaurant.id

    serializer = ReviewSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user, restaurant=restaurant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def reply_write(request, pk):
    user = User.objects.get(id=21)  # 임시 유저 지정, 추후 삭제

    try:
        review = Review.objects.get(id=pk)
    except Review.DoesNotExist:
        return Response({"error": "Review not found"}, status=status.HTTP_404_NOT_FOUND)

    data = request.data
    data["user"] = user.id
    data["review"] = review.id

    serializer = ReplySerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
