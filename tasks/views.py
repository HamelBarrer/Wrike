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


class TypeTaskListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'users:login'
    permission_required = 'tasks.view_typetask'
    template_name = 'tasks/type_task.html'
    queryset = TypeTask.objects.all().order_by('-pk')


class TypeTaskCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    login_url = 'users:login'
    permission_required = 'tasks.add_typetask'
    template_name = 'tasks/add_type_task.html'
    model = TypeTask
    form_class = TypeTaskForm
    success_url = reverse_lazy('tasks:type_task')


class TypeTaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'users:login'
    permission_required = 'tasks.change_typetask'
    template_name = 'tasks/update_type_task.html'
    model = TypeTask
    form_class = TypeTaskForm
    success_url = reverse_lazy('tasks:type_task')


class TaskListView(PermissionRequiredMixin, LoginRequiredMixin, ListView):
    login_url = 'users:login'
    permission_required = 'tasks.view_task'
    template_name = 'tasks/task.html'
    queryset = Task.objects.annotate(Count('activities')).order_by('-pk')


class TaskUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    login_url = 'users:login'
    permission_required = 'tasks.change_activities'
    template_name = 'tasks/update_task.html'
    form_class = TaskForm
    model = Task
    # success_url = reverse_lazy('tasks:task')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['perm'] = self.request.user.has_perm('tasks.view_task')
        if self.request.method == 'POST':
            context['formset'] = TaskFormSet(
                self.request.POST, instance=self.object)
        else:
            context['formset'] = TaskFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        with transaction.atomic():
            self.object = form.save()
            if formset.is_valid():
                formset.instance = self.object
                formset.save()
                if formset:
                    activities = self.object.activities_set.count()
                    completed = self.object.activities_set.filter(
                        status=True).count()
                    if activities == 0:
                        self.object.percentage = 0
                        self.object.status = False
                        self.object.save()
                    else:
                        total = (completed * 100) // activities
                        if total == 100:
                            self.object.percentage = total
                            self.object.status = True
                            self.object.save()
                        else:
                            self.object.percentage = total
                            self.object.status = False
                            self.object.save()

        if self.request.user.has_perms(['auth.add_group']):
            return redirect('tasks:task')
        else:
            return redirect('projects:project')
