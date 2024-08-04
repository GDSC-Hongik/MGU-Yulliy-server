from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


class CustomUserAdmin(UserAdmin):
    list_display = (
        "id",
        "name",
        "email",
        "profile_img",
        "reliability",
        "date_joined",
        "last_login",
    )

admin.site.register(User, CustomUserAdmin)
