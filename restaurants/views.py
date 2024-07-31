# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Restaurant, SearchHistory, UserRestaurantList
from .serializers import (
    RestaurantSerializer,
    RestaurantListSerializer,
    SearchHistorySerializer,
    UserRestaurantListSerializer,
)
from django.contrib.auth.decorators import login_required


@api_view(["GET"])
def restaurant_list(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)


@api_view(["GET", "POST"])
def search(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            histories = SearchHistory.objects.filter(user=request.user)
            serializer = SearchHistorySerializer(histories, many=True)
            return Response({"histories": serializer.data})
        else:
            return Response({"error": "User not authenticated"}, status=401)

    elif request.method == "POST":
        query = request.data.get("query", "")
        if not query:
            return Response({"error": "No search query provided"}, status=400)

        if request.user.is_authenticated:
            SearchHistory.objects.create(user=request.user, query=query)

        restaurants = Restaurant.objects.filter(name__icontains=query)
        serializer = RestaurantListSerializer(restaurants, many=True)
        return Response({"results": serializer.data})

    else:
        return Response({"error": "Unsupported method"}, status=405)


@api_view(["GET"])
@login_required
def user_restaurant_list(request):
    user_restaurants = UserRestaurantList.objects.filter(user=request.user)
    serializer = UserRestaurantListSerializer(user_restaurants, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST", "DELETE"])
@login_required
def add_remove_restaurant(request, pk):
    try:
        restaurant = Restaurant.objects.get(pk=pk)
        if request.method == "POST":
            UserRestaurantList.objects.create(user=request.user, restaurant=restaurant)
            return Response(
                {"message": "Restaurant added successfully"},
                status=status.HTTP_201_CREATED,
            )
        elif request.method == "DELETE":
            user_restaurant = UserRestaurantList.objects.get(
                user=request.user, restaurant=restaurant
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
    except UserRestaurantList.DoesNotExist:
        return Response(
            {"message": "Restaurant not found in your list"},
            status=status.HTTP_404_NOT_FOUND,
        )
