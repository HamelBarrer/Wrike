from django.contrib import admin

from .models import Profile

@admin.register(Profile)
class ProfileCustom(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at', 'updated_at')