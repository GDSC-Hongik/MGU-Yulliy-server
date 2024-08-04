from django.urls import path
from . import views

urlpatterns = [
    path(
        "friends/<int:id>/restaurants/",
        views.friend_restaurant_list,
        name="friend-restaurant-list",
    ),
    path("friends/", views.friend_list, name="friend-list"),
    path("friend-recommend/", views.friend_recommend, name="friend-recommend"),
    # 추가 기능을 테스트하기 위한 url으로 실제로는 /friend 안에서 모두 진행됨
    path("friend-request/", views.FriendRequestView.as_view(), name="friend-request"),
    path("friends/", views.friend_list, name="friend-list"),
    path("friend-recommend/", views.friend_recommend, name="friend-recommend"),
]
