from projects.views import ProjectTemplateView
from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.ProjectTemplateView.as_view(), name='home'),
    path('proyectos/', views.ProjectListView.as_view(), name='project'),
    path('crear_projecto/', views.ProjectCreateView.as_view(), name='add_project'),
    path('editar_proyecto/<slug>/', views.update_project, name='update_project'),
]
