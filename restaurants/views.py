# from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Restaurant, SearchHistory
from .serializers import (
    RestaurantSerializer,
    RestaurantListSerializer,
    SearchHistorySerializer,
)


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
