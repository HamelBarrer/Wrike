from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import View, UpdateView, CreateView, DeleteView, ListView
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


# class TaskCreateView(CreateView):
#     model = Task
#     template_name = 'tasks/add_task.html'
#     form_class = TaskForm
#     success_url = reverse_lazy('projects:project')

#     def get_context_data(self, **kwargs):
#         data = super().get_context_data(**kwargs)
#         if self.request.POST:
#             data['activities'] = TaskFormSet(self.request.POST)
#         else:
#             data['activities'] = TaskFormSet()

#         return data

#     def form_valid(self, form):
#         context = self.get_context_data()
#         activities = context['activities']
#         with transaction.atomic():
#             self.object = form.save()

#             if activities.is_valid():
#                 activities.instance = self.object
#                 activities.save()

#         return super().form_valid(form)
def create_task(request):
    template_name = 'tasks/add_task.html'
    form = TaskForm(request.POST)
    formset = TaskFormSet()

    if request.method == 'POST' and form.is_valid():
        form.save()
        with transaction.atomic():
            formset = TaskFormSet(request.POST)
            if formset.is_valid():
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
