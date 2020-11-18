from django.shortcuts import render
from django.views.generic import DetailView

from users.models import Developer
from projects.models import Project
from tasks.models import Task, Activities


class DeveloperDatailView(DetailView):
    template_name = 'dates/dates.html'
    model = Developer

    def task_percentage(self):
        projects = Project.objects.filter(developer=self.kwargs['pk'])
        data = []
        for project in projects:
            tasks = Task.objects.filter(project=project).filter(state=True).count()
            task = Task.objects.filter(project=project).filter(state=False).count()
            data.append(int((task * 100) / tasks))

        return data

    def activities_porcentage(self):
        projects = Project.objects.filter(developer=self.kwargs['pk'])
        data = []
        for project in projects:
            tasks = Task.objects.filter(project=project).filter(state=True)
            for task in tasks:
                activities = Activities.objects.filter(task=task).count()
                complete = Activities.objects.filter(task=task).filter(process=False).count()
                data.append(int((complete * 100) / activities))

            return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = Project.objects.filter(
            developer=self.kwargs['pk'])
        context['quantity'] = Project.objects.filter(
            developer=self.kwargs['pk']).count()
        context['tasks'] = self.task_percentage()
        context['activities'] = self.activities_porcentage()
        return context
