from django.urls import path
from . import views


urlpatterns = [
    path("reviews/<int:pk>/", views.reply, name="reply"),
]
