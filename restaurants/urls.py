from django.urls import path, include
from restaurants import views


urlpatterns = [
    path("restaurants/", views.restaurant_list),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
