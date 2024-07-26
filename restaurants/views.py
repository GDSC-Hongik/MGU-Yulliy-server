# from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Restaurant
from .serializers import RestaurantSerializer


@csrf_exempt
def restaurant_list(request):
    if request.method == "GET":
        restaurants = Restaurant.objects.all()
        serializer = RestaurantSerializer(restaurants, many=True)
        return JsonResponse(serializer.data, safe=False)
