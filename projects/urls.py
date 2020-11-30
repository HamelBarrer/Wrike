from projects.views import ProjectTemplateView
from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.ProjectTemplateView.as_view(), name='home'),
    path('proyectos/', views.ProjectListView.as_view(), name='project'),
    path('proyectos/crear/', views.ProjectCreateView.as_view(), name='add_project'),
    path('proyectos/editar/<slug>/', views.project_update, name='update_project'),
]
