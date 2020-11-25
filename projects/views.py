from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, TemplateView
from django.db import transaction
from django.db.models import Count

from users.models import Developer

from tasks.models import Task

from .models import Project
from .forms import ProjectForm, ProjectFormSet


class ProjectTemplateView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    template_name = 'index.html'
    paginate_by = 6
    queryset = Project.objects.annotate(Count('developer'))


class ProjectListView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    template_name = 'projects/project.html'
    queryset = Project.objects.annotate(Count('developer'))


class ProjectCreateView(LoginRequiredMixin, CreateView):
    login_url = 'users:login'
    template_name = 'projects/add_project.html'
    form_class = ProjectForm
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


class ProjectUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users:login'
    template_name = 'projects/add_project.html'
    form_class = ProjectForm
    model = Project
    success_url = reverse_lazy('projects:project')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['formset'] = ProjectFormSet(
                self.request.POST, instance=self.object)
        else:
            data['formset'] = ProjectFormSet(instance=self.object)

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
