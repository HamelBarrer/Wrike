from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.ProjectListView.as_view(), name='project'),
    path('crear_projecto/', views.ProjectCreateView.as_view(), name='add_project'),
    path('editar_proyecto/<slug>/', views.ProjectUpdateView.as_view(), name='update_project'),
]
