from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('buscador/', views.DeveloperSearchView.as_view(), name='search'),

    path('', views.login_view, name='login'),
    path('cerrar_sesion/', views.logout_view, name='logout'),
    path('registro/', views.UserCreationView.as_view(), name='register'),
]