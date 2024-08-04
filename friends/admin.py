from django.contrib import admin
from .models import Friend, FriendRequest


class FriendAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "friend", "created_at")


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ("id", "from_user", "to_user", "state", "created_at")


admin.site.register(Friend, FriendAdmin)
admin.site.register(FriendRequest, FriendRequestAdmin)
