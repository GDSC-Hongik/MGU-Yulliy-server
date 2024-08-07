from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from accounts.models import User
from restaurants.models import Restaurant
from .models import Review, Recommend
from .serializers import ReviewSerializer, ReplySerializer, ReviewListSerializer

# from rest_framework.authentication import TokenAuthentication
# from rest_framework.permissions import IsAuthenticated


@api_view(["GET", "POST"])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def review(request, pk):
    """
    한줄평 더보기 기능 (GET)
    한줄평 작성 기능 (POST)
    """
    if request.method == "GET":
        # 리뷰 조회 기능
        reviews = Review.objects.filter(restaurant_id=pk).order_by("-date")
        serializer = ReviewListSerializer(reviews, many=True)
        return Response({"results": serializer.data}, status=status.HTTP_200_OK)

    elif request.method == "POST":
        # 리뷰 작성 기능
        try:
            restaurant = Restaurant.objects.get(pk=pk)
        except Restaurant.DoesNotExist:
            return Response(
                {"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND
            )

        user = User.objects.get(id=21)  # 임시 유저 지정, 추후 삭제

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


@api_view(["POST"])
def evaluate_review(request, restaurant_id, review_id):
    """
    한줄평 평가 기능 (좋아요/싫어요)
    """
    try:
        review = Review.objects.get(id=review_id, restaurant_id=restaurant_id)
        user = User.objects.get(id=21)  # 임시 유저 지정, 추후 삭제

        # 사용자가 이미 평가했는지 확인
        recommend_entry, created = Recommend.objects.get_or_create(
            user=user, review=review
        )

        evaluation = request.data.get("evaluation")
        if evaluation == "1":
            # 좋아요
            if created or recommend_entry.recommend != 1:
                review.recommend_count += 1
                if recommend_entry.recommend == 0:  # 이전에 싫어요였던 경우
                    review.decommend_count -= 1
                recommend_entry.recommend = 1

        elif evaluation == "0":
            # 싫어요
            if created or recommend_entry.recommend != 0:
                review.decommend_count += 1
                if recommend_entry.recommend == 1:  # 이전에 좋아요였던 경우
                    review.recommend_count -= 1
                recommend_entry.recommend = 0

        else:
            return Response(
                {"message": "Invalid evaluation value"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        review.save()
        recommend_entry.save()

        return Response(
            {"message": "Review evaluated successfully"}, status=status.HTTP_200_OK
        )

    except Review.DoesNotExist:
        return Response(
            {"message": "Review not found"}, status=status.HTTP_404_NOT_FOUND
        )
