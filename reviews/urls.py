from django.urls import path
from . import views


urlpatterns = [
    path("reviews/<int:pk>/", views.reply_write, name="reply-write"),
]
