from django.shortcuts import render
from django.views.generic import DetailView

from users.models import Developer, User
from tasks.models import Task

from .models import Date


class DeveloperDatailView(DetailView):
    template_name = 'dates/dates.html'
    model = Developer
    pk_url_kwarg = 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        print(self.pk_url_kwarg)
        context['quantity'] = Task.objects.all().filter(developer=2).count()
        return context
