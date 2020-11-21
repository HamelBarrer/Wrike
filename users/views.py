from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy

from .models import Developer
from .forms import UserForm


def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:home')

    template_name = 'users/login.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            messages.success(request, f'Bienvenido {user.username}')
            return redirect('projects:home')
        else:
            messages.error(request, 'Usuario o contraseña invalidos')

    return render(request, template_name)


def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada exitosamente')
    return redirect('users:login')


class UserCreationView(PermissionRequiredMixin, LoginRequiredMixin, CreateView):
    login_url = 'users:login'
    permission_required = 'users.can_add_user'
    template_name = 'users/register.html'
    form_class = UserForm
    success_url = reverse_lazy('projects:home')


class DeveloperSearchView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    template_name = 'users/search.html'

    def get_queryset(self):
        return Developer.objects.filter(user__username__icontains=self.query())

    def query(self):
        return self.request.GET.get('q')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.query()
        return context
