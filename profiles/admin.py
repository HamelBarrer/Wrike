from django.contrib import admin

from .models import (
    ProfileAdministrator,
    ProfileDeveloper,
)


@admin.register(ProfileAdministrator)
class ProfileAdminCustom(admin.ModelAdmin):
    fields = ('user',)
    list_display = ('__str__', 'created_at')


@admin.register(ProfileDeveloper)
class ProfileDevelopCustom(admin.ModelAdmin):
    fields = ('user',)
    list_display = ('__str__', 'created_at')
