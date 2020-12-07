"""wrike URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import handler403, handler404
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from users.views import error_403, error_404
from django.conf.urls.static import static

handler403 = error_403
handler404 = error_404

urlpatterns = [
    path('', include('projects.urls')),
    path('tareas/', include('tasks.urls')),
    path('acceder/', include('users.urls')),
    path('perfil/', include('profiles.urls')),
    path('admin/', admin.site.urls),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,
)
