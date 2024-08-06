from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from restaurants.models import Restaurant
from .models import Review
from .serializers import ReviewSerializer

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

    request.data["user"] = user.id
    request.data["restaurant"] = restaurant.id

    try:
        data = request.data
    except ValueError:
        return Response({"detail": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

    parent_id = data.get("parent")
    if parent_id:
        try:
            parent_review = Review.objects.get(id=parent_id)
            if parent_review.parent is not None:
                return Response(
                    {"error": "Replies to replies are not allowed"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            data["parent"] = parent_review.id
        except Review.DoesNotExist:
            return Response(
                {"error": "Parent review not found"}, status=status.HTTP_404_NOT_FOUND
            )

    serializer = ReviewSerializer(data=data)
    if serializer.is_valid():
        serializer.save(user=user, restaurant=restaurant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
