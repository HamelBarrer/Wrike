from django.contrib import admin

from .models import (
    ProfileAdministrator,
    ProfileDeveloper,
)

admin.site.register(ProfileAdministrator)
admin.site.register(ProfileDeveloper)
