# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Restaurant, SearchHistory, UserRestaurantsList
from .serializers import (
    RestaurantSerializer,
    RestaurantListSerializer,
    SearchHistorySerializer,
    RestaurantlistSerializer,
    RestaurantDetailSerializer,
)

# from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
import logging
from accounts.models import User  # 임시 유저 지정을 위한 임포트, 추후 삭제
from django.db.models import Q, Subquery, OuterRef
from django.utils import timezone


@csrf_exempt
@api_view(["GET"])
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST", "DELETE"])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search(request):
    user = User.objects.get(id=21)  # 임시 유저 지정, 추후 삭제
    if request.method == "GET":
        latest_searches = SearchHistory.objects.filter(
            user=user,
            id=Subquery(
                SearchHistory.objects.filter(user=user, query=OuterRef("query"))
                .order_by("-timestamp")
                .values("id")[:1]
            ),
        )
        serializer = SearchHistorySerializer(latest_searches, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        query = request.data.get("query", "")
        if not query:
            return Response(
                {"error": "No search query provided"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        existing_history = SearchHistory.objects.filter(
            user=user, query=query
        ).first()  # 추후 삭제
        # existing_history = SearchHistory.objects.filter(user=request.user, query=query).first()

        if existing_history:
            existing_history.timestamp = timezone.now()
            existing_history.save()
        else:
            SearchHistory.objects.create(user=user, query=query)  # 추후 삭제
            # SearchHistory.objects.create(user=request.user, query=query)

        query_terms = query.split()
        q_objects = Q()
        for term in query_terms:
            q_objects &= Q(name__icontains=term) | Q(food_type__icontains=term)

        restaurants = Restaurant.objects.filter(q_objects).distinct()
        serializer = RestaurantListSerializer(restaurants, many=True)
        data = serializer.data
        logging.debug("Serialized data: %s", data)
        return Response(data)

    elif request.method == "DELETE":
        history_id = request.data.get("id", "")
        if not history_id:
            return Response(
                {"error": "No history ID provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            history_to_delete = SearchHistory.objects.get(id=history_id, user=user)
            history_to_delete.delete()
            return Response({"message": "Search history deleted successfully"})
        except SearchHistory.DoesNotExist:
            return Response(
                {"error": "No matching search history found"},
                status=status.HTTP_404_NOT_FOUND,
            )

    else:
        return Response(
            {"error": "Unsupported method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


@csrf_exempt
@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def user_restaurant_list(request):
    try:
        user = User.objects.get(id=21)  # 임시 유저 지정, 추후 삭제
        user_restaurants = UserRestaurantsList.objects.filter(user=user)  # 추후 삭제
        # user_restaurants = UserRestaurantsList.objects.filter(user=request.user)
        restaurant_ids = user_restaurants.values_list("restaurant_id", flat=True)
        restaurants = Restaurant.objects.filter(id__in=restaurant_ids)
        serializer = RestaurantlistSerializer(restaurants, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response(
            {"message": "Default user not found"}, status=status.HTTP_404_NOT_FOUND
        )


@csrf_exempt
@api_view(["POST", "DELETE"])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_remove_restaurant(request, pk):
    user = User.objects.get(id=21)  # 임시 유저 지정, 추후 삭제
    try:
        restaurant = Restaurant.objects.get(pk=pk)
        if request.method == "POST":
            UserRestaurantsList.objects.create(
                user=user, restaurant=restaurant
            )  # 추후 삭제
            # UserRestaurantsList.objects.create(user=request.user, restaurant=restaurant)
            return Response(
                {"message": "Restaurant added successfully"},
                status=status.HTTP_201_CREATED,
            )
        elif request.method == "DELETE":
            user_restaurant = UserRestaurantsList.objects.get(
                # user=request.user, restaurant=restaurant
                user=user,
                restaurant=restaurant,  # 추후 삭제
            )
            user_restaurant.delete()
            return Response(
                {"message": "Restaurant deleted successfully"},
                status=status.HTTP_204_NO_CONTENT,
            )
    except Restaurant.DoesNotExist:
        return Response(
            {"message": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND
        )
    except UserRestaurantsList.DoesNotExist:
        return Response(
            {"message": "Restaurant not found in your list"},
            status=status.HTTP_404_NOT_FOUND,
        )


@api_view(["GET"])
# @authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def restaurant_detail(request, pk):
    try:
        restaurant = Restaurant.objects.prefetch_related("reviews").get(pk=pk)
        serializer = RestaurantDetailSerializer(restaurant)
        return Response(serializer.data)
    except Restaurant.DoesNotExist:
        return Response(
            {"message": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND
        )
