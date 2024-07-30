from django.urls import path, include
from . import views


urlpatterns = [
    #    path("restaurants/", views.restaurant_list, name="restaurant-list"),
    path("restaurants/", views.user_restaurant_list, name="user-restaurant-list"),
    path("restaurants/<int:pk>/", views.add_restaurant, name="add-restaurant"),
    path("restaurants/<int:pk>/", views.remove_restaurant, name="remove-restaurant"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
