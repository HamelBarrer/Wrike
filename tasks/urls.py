from django.urls import path

from . import views

app_name = 'tasks'
urlpatterns = [
    # Urls for the views of type_task
    path('tipo_tarea/', views.TypeTaskListView.as_view(), name='type_task'),
    path('tipo_tarea/crear/', views.TypeTaskCreateView.as_view(), name='add_type_task'),
    path('tipo_tarea/actualizar/<slug>/', views.TypeTaskUpdateView.as_view(), name='update_type_task'),

    # Urls for the views of task
    path('tareas/', views.TaskListView.as_view(), name='task'),
    path('crear_tarea/', views.create_task, name='add_task'),
    path('actualizar_tarea/<slug>', views.TaskUpdateView.as_view(), name='update_task'),
    path('eliminar_tarea/<slug>', views.TaskDeleteView.as_view(), name='delete_task'),

]
