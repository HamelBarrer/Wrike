from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.db import transaction

from tasks.models import Task

from .models import Project
from .forms import ProjectForm, ProjectFormSet


class ProjectListView(ListView):
    template_name = 'projects/project.html'
    queryset = Project.objects.all().order_by('-pk')

class ProjectCreateView(CreateView):
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

# def create_project(request):
#     template_name = 'projects/add_project.html'
#     form = ProjectForm()
#     formset = ProjectFormSet()

#     if request.method == 'POST':
#         form = ProjectForm(request.POST)
#         formset = ProjectFormSet(request.POST)

#         if form.is_valid():
#             instance = form.save(commit=False)
#             instance.save()

#             if formset.is_valid():
#                 formset.instance = instance
#                 formset.save()

#                 return redirect('projects:project')

#     return render(request, template_name, {
#         'form': form,
#         'formset': formset,
#     })


# class ProjectUpdateView(UpdateView):
#     template_name = 'projects/update_project.html'
#     form_class = ProjectForm
#     model = Project
#     success_url = reverse_lazy('projects:project')

def update_project(request, slug):
    project = Project.objects.get(slug=slug)
    template_name = 'projects/update_project.html'
    form = ProjectForm(instance=project)
    formset = ProjectFormSet(instance=project)

    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        formset = ProjectFormSet(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            formset = ProjectFormSet(request.POST, instance=task)

            if formset.is_valid():
                task.save()
                formset.save()

                return redirect('projects:project')

    return render(request, template_name, {
        'form': form,
        'formset': formset,
    })
