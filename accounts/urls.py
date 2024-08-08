from django.urls import path
from .views import RegisterView, LoginView, profile

urlpatterns = [
    path("auth/register/", RegisterView.as_view()),
    path("auth/login/", LoginView.as_view()),
    path("profile/", profile, name="profile"),
]
