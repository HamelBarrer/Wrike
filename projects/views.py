from django.shortcuts import render
from django.views.generic import ListView, CreateView

from .models import Project
from .forms import ProjectForm


class ProjectListView(ListView):
    template_name = 'projects/project.html'
    queryset = Project.objects.all().order_by('-pk')
