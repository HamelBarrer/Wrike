from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView, CreateView, DeleteView, ListView
from django.db import transaction
from django.db.models import Count

from users.models import Developer

from .models import (
    Activities,
    TypeTask,
    Task,
)

from .forms import (
    TypeTaskForm,
    TaskForm,
    TaskFormSet,
)


class TypeTaskListView(LoginRequiredMixin, ListView):
    template_name = 'tasks/type_task.html'
    queryset = TypeTask.objects.all().order_by('-pk')


class TypeTaskCreateView(LoginRequiredMixin, CreateView):
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


# class TaskCreateView(LoginRequiredMixin, CreateView):
#     login_url = 'users:login'
#     template_name = 'projects/add_project.html'
#     form_class = TaskForm
#     success_url = reverse_lazy('projects:project')

#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         if self.request.POST:
#             data['formset'] = TaskFormSet(self.request.POST)
#         else:
#             data['formset'] = TaskFormSet()

#         return data

#     def form_valid(self, form):
#         context = self.get_context_data()
#         formset = context['formset']

#         with transaction.atomic():
#             self.object = form.save()

#             if formset.is_valid():
#                 formset.instance = self.object
#                 formset.save()

#         return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users:login'
    template_name = 'tasks/update_task.html'
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks:task')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = TaskFormSet(
                self.request.POST, instance=self.object)
        else:
            data['formset'] = TaskFormSet(instance=self.object)

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        with transaction.atomic():
            self.object = form.save()

            if formset.is_valid():
                formset.instance = self.object
                formset.save()

        return super().form_valid(form)
