from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    # Urls for the views of type_task
    path('tipo_tarea/', views.TypeTaskListView.as_view(), name='type_task'),
    path('tipo_tarea/crear/', views.TypeTaskCreateView.as_view(), name='add_type_task'),
    path('tipo_tarea/actualizar/<slug>/', views.TypeTaskUpdateView.as_view(), name='update_type_task'),

    # Urls for the views of task
    path('', views.TaskListView.as_view(), name='task'),
    # path('tareas/crear/', views.TaskCreateView.as_view(), name='add_task'),
    path('tareas/actualizar/<slug>', views.task_update, name='update_task'),
]
