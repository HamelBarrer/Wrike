from django.http import JsonResponse
from django.core import serializers
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, UpdateView, CreateView, DeleteView, ListView

from users.models import Developer
from projects.models import Project

from .models import (
    Activities,
    TypeTask,
    Task,
)

from .forms import (
    TypeTaskForm,
    TaskForm,
)


class DeveloperListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    login_url = 'users:login'
    permission_required = 'tasks.can_view_user'
    template_name = 'index.html'
    queryset = Developer.objects.all().order_by('-pk')


class TypeTaskView(PermissionRequiredMixin, LoginRequiredMixin, View):
    login_url = 'users:login'
    permission_required = 'type_task.can_add_type_task'
    template_name = 'tasks/add_type_task.html'
    form_class = TypeTaskForm
    model = TypeTask

    def get_query_set(self):
        query = self.model.objects.all().order_by('-pk')
        return query

    def get_context_data(self, **kwargs):
        context = {}
        context['type_tasks'] = self.get_query_set()
        context['form'] = self.form_class
        return context

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            return redirect('tasks:type_task')


class TypeTaskUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = 'users:login'
    permission_required = 'type_task.can_change_type_task'
    template_name = 'tasks/update_type_task.html'
    form_class = TypeTaskForm
    model = Task
    success_url = reverse_lazy('tasks:type_task')


class TypeTaskDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = 'users:login'
    permission_required = 'type_task.can_delete_type_task'
    template_name = 'tasks/delete_type_task.html'
    form_class = TypeTaskForm
    model = Task
    success_url = reverse_lazy('tasks:type_task')


class TaskListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    login_url = 'users:login'
    permission_required = 'tasks.can_view_user'
    template_name = 'tasks/task.html'
    queryset = Task.objects.all().order_by('-pk')


# def task_create(request):
#     template_name = 'tasks/add_task.html'
#     form_class = TaskForm(request.POST)

#     if request.method == 'POST' and form_class.is_valid():
#         form_class.save()
#         return redirect('tasks:task')

#     return render(request, template_name, {
#         'form': form_class,
#     })


def activities_create(request):
    if request.is_ajax and request.method == 'POST':
        form = Activities(request.POST)
        if form.is_valid():
            instance = form.save()
            serializer = serializers.serialize('json', [instance])
            return JsonResponse({'instance': serializer}, status=200)
        else:
            return JsonResponse({'error': form.errors}, status=400)

    return JsonResponse({'error': ''}, status=400)

class TaskCreateView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = 'users:login'
    permission_required = 'tasks.can_add_user'
    template_name = 'tasks/add_task.html'
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks:task')

    def get_queryset(self):
        return Project.objects.all().exists()


class TaskUpdateView(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
    login_url = 'users:login'
    permission_required = 'tasks.can_change_user'
    template_name = 'tasks/update_task.html'
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks:task')


class TaskDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = 'users:login'
    permission_required = 'tasks.can_delete_user'
    template_name = 'tasks/delete_task.html'
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks:task')
