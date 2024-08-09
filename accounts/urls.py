from django.urls import path, include
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    UserViewSet,
    DeleteUserView,
    profile,
)

# 뷰셋
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

router = routers.DefaultRouter()
router.register("list", UserViewSet)

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("logout/", LogoutView.as_view()),
    path("test/", include(router.urls)),
    path("delete/", DeleteUserView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),  # jwt 토큰 재발급
    path("profile/", profile, name="profile"),
]
