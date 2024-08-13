from django.urls import path
from .views import (
    RegisterView,
    LoginView,
    DeleteUserView,
    profile,
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("register/", RegisterView.as_view()),
    path("login/", LoginView.as_view()),
    path("delete-user/", DeleteUserView.as_view()),
    path("refresh/", TokenRefreshView.as_view()),  # jwt 토큰 재발급
    path("profile/", profile, name="profile"),
]
