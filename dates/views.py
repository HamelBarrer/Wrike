from django.shortcuts import render
from django.views.generic import DetailView

from users.models import Developer
from projects.models import Project

from .models import Date


class DeveloperDatailView(DetailView):
    template_name = 'dates/dates.html'
    model = Developer

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['quantity'] = Project.objects.filter(
            developer=self.kwargs['pk']).count()
        return context
