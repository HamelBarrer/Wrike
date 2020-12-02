from users.models import Developer
from tasks.models import Task
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.db import transaction
from django.db.models import Count

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
            developer = Developer.objects.filter(
                user=self.request.user).first()
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
            developer = Developer.objects.filter(
                user=self.request.user).first()
            return Project.objects.filter(developer=developer)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['group'] = self.request.user.groups.filter(
            name='administradores').exists()

        return context


class ProjectView(DetailView):
    template_name = 'projects/view_project.html'

    def get_queryset(self):
        developer = Developer.objects.filter(user=self.request.user).first()
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


def project_update(request, slug):
    template_name = 'projects/update_project.html'

    instancia = Project.objects.get(slug=slug)
    form = ProjectForm(instance=instancia)
    formset = ProjectFormSet(instance=instancia)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=instancia)
        formset = ProjectFormSet(request.POST, instance=instancia)

        if form.is_valid():
            instancia = form.save(commit=False)

            if formset.is_valid():
                formset.instance = instancia

                formset.save()

                activities = instancia.task_set.count()
                completed = instancia.task_set.filter(
                    state=True).count()
                total = (completed * 100) // activities
                if total == 100:
                    instancia.porcentage = total
                    Project.objects.update(status='approver')
                    instancia.save()
                else:
                    instancia.porcentage = total
                    Project.objects.update(status='process')
                    instancia.save()

            return redirect('projects:project')

    return render(request, template_name, {
        'form': form,
        'formset': formset,
    })
