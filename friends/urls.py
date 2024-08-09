from django.urls import path
from . import views

urlpatterns = [
    path(
        "friends/<int:pk>/restaurants/",
        views.friend_restaurant_list,
        name="friend-restaurant-list",
    ),
    path("friends/", views.friends, name="friends"),
    path("friend-recommend/", views.friend_recommend, name="friend-recommend"),
]
