from django.shortcuts import render
from django.views.generic import ListView

from .models import (
    TypeTask,
    Task,
)

from .forms import (
    TypeTaskForm,
    TaskForm,
)


class TaskListView(ListView):
    template_name = 'index.html'
    queryset = Task.objects.all().order_by('-pk')
