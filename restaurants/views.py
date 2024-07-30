# from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant, UserRestaurantList
from .serializers import RestaurantSerializer, UserRestaurantListSerializer
from django.contrib.auth.decorators import login_required


@csrf_exempt
def restaurant_list(request):
    if request.method == "GET":
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@login_required
def user_restaurant_list(request):
    if request.method == "GET":
        user_restaurants = UserRestaurantList.objects.filter(user=request.user)
        serializer = UserRestaurantListSerializer(user_restaurants, many=True)
        return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@login_required
def add_restaurant(request, pk):
    if request.method == "POST":
        try:
            restaurant = Restaurant.objects.get(pk=pk)
            UserRestaurantList.objects.create(user=request.user, restaurant=restaurant)
            return JsonResponse(
                {"message": "Restaurant added successfully"}, status=201
            )
        except Restaurant.DoesNotExist:
            return JsonResponse({"message": "Restaurant not found"}, status=404)


@csrf_exempt
@login_required
def remove_restaurant(request, pk):
    if request.method == "DELETE":
        try:
            user_restaurant = UserRestaurantList.objects.get(
                user=request.user, restaurant_id=pk
            )
            user_restaurant.delete()
            return JsonResponse(
                {"message": "Restaurant deleted successfully"}, status=204
            )
        except UserRestaurantList.DoesNotExist:
            return JsonResponse(
                {"message": "Restaurant not found in your list"}, status=404
            )
