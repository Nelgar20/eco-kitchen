from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    display_fields = ("user", "display_name", "created_on")
    search_fields = ("user__username", "user__email", "display_name")
