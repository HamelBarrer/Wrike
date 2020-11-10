from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from .models import Project
from .forms import ProjectForm


class ProjectListView(ListView):
    template_name = 'projects/project.html'
    queryset = Project.objects.all().order_by('-pk')


class ProjectCreateView(CreateView):
    template_name = 'projects/add_project.html'
    form_class = ProjectForm
    model = Project
    success_url = reverse_lazy('projects:project')


class ProjectUpdateView(UpdateView):
    template_name = 'projects/update_project.html'
    form_class = ProjectForm
    model = Project
    success_url = reverse_lazy('projects:project')
