from tasks.views import TaskListView
from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    # Urls for the views of type_task
    path('tipo_tarea', views.TypeTaskView.as_view(), name='type_task'),
    path('actualizar_tipo_tarea/<slug>', views.TaskUpdateView.as_view(), name='update_type_task'),
    path('eliminar_tipo_tarea/<slug>', views.TaskDeleteView.as_view(), name='delete_type_task'),

    # Urls for the views of task
    path('', views.DeveloperListView.as_view(), name='developer_task'),
    path('tareas/', views.TaskListView.as_view(), name='task'),
    path('crear_tarea/', views.TaskCreateView.as_view(), name='add_task'),
    path('actualizar_tarea/<slug>', views.TaskUpdateView.as_view(), name='update_task'),
    path('eliminar_tarea/<slug>', views.TaskDeleteView.as_view(), name='delete_task'),

]
