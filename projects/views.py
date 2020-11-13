from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.db import transaction

from .models import Project
from .forms import ProjectForm, ProjectFormSet


class ProjectListView(ListView):
    template_name = 'projects/project.html'
    queryset = Project.objects.all().order_by('-pk')


class ProjectCreateView(CreateView):
    template_name = 'projects/add_project.html'
    form_class = ProjectForm
    model = Project
    success_url = reverse_lazy('projects:project')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['task'] = ProjectFormSet(self.request.POST)
        else:
            data['task'] = ProjectFormSet()

        return data

    def form_valid(self, form):
        context = self.get_context_data()
        task = context['task']
        with transaction.atomic():
            self.object = form.save()

            if task.is_valid():
                task.instance = self.object
                task.save()

        return super().form_valid(form)


class ProjectUpdateView(UpdateView):
    template_name = 'projects/update_project.html'
    form_class = ProjectForm
    model = Project
    success_url = reverse_lazy('projects:project')
