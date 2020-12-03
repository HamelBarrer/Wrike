from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Developer, Administrator


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Roles', {'fields': ('role',)}),
        ('Avatar', {'fields': ('avatar',)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role', 'avatar')}),
    )


admin.site.register(Developer)
admin.site.register(Administrator)
