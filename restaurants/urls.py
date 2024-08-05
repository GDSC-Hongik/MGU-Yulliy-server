from django.urls import path, include, re_path
from . import views


urlpatterns = [
    # path("restaurants/", views.restaurant_list, name="restaurant-list"),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("search/", views.search, name="search"),
    re_path(r"^search$", views.search),
    path(
        "restaurants/<int:pk>/",
        views.add_remove_restaurant,
        name="add-remove-restaurant",
    ),
    path(
        "restaurants/<int:pk>/detail", views.restaurant_detail, name="restaurant-detail"
    ),
    path("restaurants/", views.user_restaurant_list, name="user-restaurant-list"),
]
