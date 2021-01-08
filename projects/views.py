from tasks.models import Task
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db import transaction
from django.db.models import Count

from users.models import User

from .models import Project
from .forms import ProjectForm, ProjectFormSet


class ProjectTemplateView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    template_name = 'index.html'
    queryset = Project.objects.annotate(developer_count=Count('developer')).order_by('-pk')
    paginate_by = 6

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        is_admin = self.request.user.has_perm('auth.add_group')

        if is_admin:
            return qs.annotate(Count('developer'))
        else:
            return qs.filter(developer=self.request.user).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['group'] = User.objects.filter(
            pk=self.request.user.pk, groups__name='administradores').exists()
        context['admin'] = User.objects.filter(
            groups__name='administradores').count()
        context['developer'] = User.objects.filter(
            groups__name='desarrolladores').count()
        context['projects'] = Project.objects.count()
        context['tasks'] = Task.objects.count()

        return context


class ProjectListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    login_url = 'users:login'
    permission_required = 'projects.view_project'
    template_name = 'projects/project.html'
    queryset = Project.objects.all().order_by('-pk')

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        is_admin = self.request.user.has_perm('auth.add_group')

        if is_admin:
            return qs.annotate(Count('developer'))
        else:
            return qs.filter(developer=self.request.user).order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


class ProjectView(LoginRequiredMixin, DetailView):
    login_url = 'users:login'
    template_name = 'projects/view_project.html'

    def get_queryset(self):
        developer = User.objects.filter(pk=self.request.user.pk).first()
        return Project.objects.filter(developer=developer).annotate(Count('task__activities'))


class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'users:login'
    template_name = 'projects/add_project.html'
    form_class = ProjectForm
    permission_required = 'projects.add_project'
    success_message = 'Proyecto creado exitosamente'
    success_url = reverse_lazy('projects:project')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ProjectFormSet(self.request.POST)
        else:
            data['formset'] = ProjectFormSet()

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


class ProjectFormView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = 'projects.change_project'
    login_url = 'users:login'
    template_name = 'projects/update_project.html'
    form_class = ProjectForm
    model = Project
    success_url = reverse_lazy('projects:project')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['formset'] = ProjectFormSet(
                self.request.POST, instance=self.object)
        else:
            context['formset'] = ProjectFormSet(instance=self.object)
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
                    activities = self.object.task_set.count()
                    completed = self.object.task_set.filter(
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

        return super().form_valid(form)
