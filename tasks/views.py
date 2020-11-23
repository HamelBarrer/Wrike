from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import UpdateView, CreateView, DeleteView, ListView
from django.db import transaction

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
    queryset = Task.objects.all().order_by('-pk')


def create_task(request):
    template_name = 'tasks/add_task.html'
    form = TaskForm()
    formset = TaskFormSet()

    if request.method == 'POST':
        form = TaskForm(request.POST)
        formset = TaskFormSet(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            formset = TaskFormSet(request.POST, instance=task)

            if formset.is_valid():
                task.save()
                formset.save()

                return redirect('projects:project')

    return render(request, template_name, {
        'form': form,
        'formset': formset,
    })


class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/add_task.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['name'] = TaskFormSet(self.request.POST, instance=self.object)
        else:
            data['name'] = TaskFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        self.object = form.save()

    def get_success_url(self):
        return reverse_lazy('mycollections:collection_detail')


class TaskDeleteView(PermissionRequiredMixin, LoginRequiredMixin, DeleteView):
    login_url = 'users:login'
    permission_required = 'tasks.can_delete_user'
    template_name = 'tasks/delete_task.html'
    form_class = TaskForm
    model = Task
    success_url = reverse_lazy('tasks:task')
