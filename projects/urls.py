from projects.views import ProjectTemplateView
from django.urls import path

from . import views

app_name = 'projects'
urlpatterns = [
    path('', views.ProjectTemplateView.as_view(), name='home'),
    path('proyectos/', views.ProjectListView.as_view(), name='project'),
    path('proyectos/ver/<slug>/', views.ProjectView.as_view(), name='view_project'),
    path('proyectos/crear/', views.ProjectCreateView.as_view(), name='add_project'),
    path('proyectos/editar/<slug>/', views.ProjectFormView.as_view(), name='update_project'),
]
