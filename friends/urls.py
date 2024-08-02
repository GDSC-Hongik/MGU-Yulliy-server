from django.urls import path
from . import views

urlpatterns = [
    path(
        "<int:id>/restaurants/",
        views.friend_restaurant_list,
        name="friend-restaurant-list",
    ),
]
