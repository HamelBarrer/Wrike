from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy

from .models import Developer, User
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


class UserListView(LoginRequiredMixin, ListView):
    login_url = 'users:login'
    template_name = 'users/users.html'
    queryset = User.objects.all().order_by('-pk')


class UserCreationView(LoginRequiredMixin, CreateView):
    login_url = 'users:login'
    template_name = 'users/register.html'
    model = User
    form_class = UserForm
    success_url = reverse_lazy('users:user')


class UserUpdateView(LoginRequiredMixin, UpdateView):
    login_url = 'users:login'
    template_name = 'users/update_user.html'
    form_class = UserForm
    model = User
    success_url = reverse_lazy('users:user')


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
