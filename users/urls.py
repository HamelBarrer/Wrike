from django.urls import path

from . import views

app_name = 'users'
urlpatterns = [
    path('', views.login_view, name='login'),
    path('cerrar_sesion/', views.logout_view, name='logout'),
    path('usuarios/', views.UserListView.as_view(), name='user'),
    path('usuarios/registro/', views.UserCreationView.as_view(), name='register'),
    path('usuarios/actualizar/<pk>/', views.UserUpdateView.as_view(), name='update'),
]
