from django.urls import path
from . import views

urlpatterns = [
    path(
        "friends/<int:id>/restaurants/",
        views.friend_restaurant_list,
        name="friend-restaurant-list",
    ),
    path("friends/", views.friend_list, name="friend-list"),
]
