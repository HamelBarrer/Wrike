from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView, FormView
from django.db import transaction
from django.db.models import Count

from users.models import User

from .models import Project
from .forms import ProjectForm, ProjectFormSet


class ProjectTemplateView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    template_name = 'index.html'
    paginate_by = 6
    # queryset = Project.objects.annotate(Count('developer')).order_by('-pk')

    def get_queryset(self):
        group = self.request.user.groups.filter(
            name='administradores').exists()
        if group:
            return Project.objects.annotate(Count('developer')).order_by('-pk')
        else:
            developer = User.objects.filter(pk=self.request.user.pk).first()
            return Project.objects.filter(developer=developer).order_by('-pk')


class ProjectListView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    template_name = 'projects/project.html'
    # queryset = Project.objects.annotate(Count('developer'))

    def get_queryset(self):
        group = self.request.user.groups.filter(name='administradores')
        if group:
            return Project.objects.annotate(Count('developer'))
        else:
            developer = User.objects.filter(pk=self.request.user.pk).first()
            return Project.objects.filter(developer=developer)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['group'] = self.request.user.groups.filter(
            name='administradores').exists()

        return context


class ProjectView(DetailView):
    template_name = 'projects/view_project.html'

    def get_queryset(self):
        developer = User.objects.filter(pk=self.request.user.pk).first()
        return Project.objects.filter(developer=developer).annotate(Count('task__activities'))


class ProjectCreateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = 'users:login'
    template_name = 'projects/add_project.html'
    form_class = ProjectForm
    permission_required = 'projects.can_add_project'
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


class ProjectFormView(UpdateView):
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
                    completed = self.object.task_set.filter(state=True).count()
                    if activities == 0:
                        self.object.porcent = 0
                        self.object.status = 'inactive'
                        self.object.save()
                    else:
                        total = (completed * 100) // activities
                        if total == 100:
                            self.object.porcent = total
                            self.object.status = 'approver'
                            self.object.save()
                            print(self.object.porcent)

        return super().form_valid(form)
