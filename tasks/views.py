from projects.models import Project
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView, CreateView, ListView
from django.db import transaction
from django.db.models import Count


from .models import (
    TypeTask,
    Task,
)

from .forms import (
    TypeTaskForm,
    TaskForm,
    TaskFormSet,
)


class TypeTaskListView(LoginRequiredMixin, PermissionRequiredMixin,ListView):
    login_url = 'users:login'
    permission_required = 'tasks.can_view_tipo_tarea'
    template_name = 'tasks/type_task.html'
    queryset = TypeTask.objects.all().order_by('-pk')


class TypeTaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'users:login'
    permission_required = 'tasks.can_add_tipo_tarea'
    template_name = 'tasks/add_type_task.html'
    model = TypeTask
    form_class = TypeTaskForm
    success_url = reverse_lazy('tasks:type_task')


class TypeTaskUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users:login'
    template_name = 'tasks/update_type_task.html'
    model = TypeTask
    form_class = TypeTaskForm
    success_url = reverse_lazy('tasks:type_task')


class TaskListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    login_url = 'users:login'
    permission_required = 'tasks.can_view_user'
    template_name = 'tasks/task.html'
    queryset = Task.objects.annotate(Count('activities')).order_by('-pk')


def task_update(request, slug):
    template_name = 'tasks/update_task.html'

    instancia = Task.objects.get(slug=slug)
    form = TaskForm(instance=instancia)
    formset = TaskFormSet(instance=instancia)

    if request.method == 'POST':
        form = TaskForm(request.POST, instance=instancia)
        formset = TaskFormSet(request.POST, instance=instancia)

        if form.is_valid():
            instancia = form.save(commit=False)

            if formset.is_valid():
                formset.instance = instancia

                formset.save()

                activities = instancia.activities_set.count()
                completed = instancia.activities_set.filter(
                    process=True).count()
                total = (completed * 100) // activities
                if total == 100:
                    instancia.state = True
                    instancia.porcentage = total
                    instancia.save()
                else:
                    instancia.state = False
                    instancia.porcentage = total
                    instancia.save()

                return redirect('tasks:task')

    return render(request, template_name, {
        'form': form,
        'formset': formset,
    })
