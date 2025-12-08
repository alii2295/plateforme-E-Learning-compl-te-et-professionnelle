from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_instructor', 'location', 'created_at']
    list_filter = ['is_instructor', 'created_at']
    search_fields = ['user__username', 'location']