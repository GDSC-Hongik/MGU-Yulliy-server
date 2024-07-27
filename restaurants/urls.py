from django.urls import path, include
from . import views


urlpatterns = [
    path("restaurants/", views.restaurant_list, name="restaurant-list"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
