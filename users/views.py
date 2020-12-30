from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import Group, Permission
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy

from .models import User
from .forms import UserForm, RoleUser


def error_403(request, exception):
    template_name = 'errors/403.html'

    return render(request, template_name)


def error_404(request, exception):
    template_name = 'errors/404.html'

    return render(request, template_name)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('projects:home')

    template_name = 'users/login.html'

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, f'Bienvenido {user.username}')
                return redirect('projects:home')
        else:
            messages.error(request, 'Usuario o contraseña invalidos')

    return render(request, template_name)


@login_required(login_url='users:login')
def logout_view(request):
    logout(request)
    messages.success(request, 'Sesion cerrada exitosamente')
    return redirect('users:login')


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    permission_required = 'users.view_user'
    login_url = 'users:login'
    template_name = 'users/users.html'
    queryset = User.objects.all().order_by('-pk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['group'] = Group.objects.values_list('name', flat=True)

        return context


class UserCreationView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, CreateView):
    permission_required = 'users.add_user'
    login_url = 'users:login'
    template_name = 'users/register.html'
    model = User
    form_class = UserForm
    success_message = 'El usuario fue creado exitosamente'
    success_url = reverse_lazy('users:user')


class UserUpdateView(LoginRequiredMixin, PermissionRequiredMixin, SuccessMessageMixin, UpdateView):
    permission_required = 'users.change_user'
    login_url = 'users:login'
    template_name = 'users/update_user.html'
    form_class = UserForm
    model = User
    success_message = 'El usuario fue modificado exitosamente'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.groups.clear()
        self.object.groups.add(self.request.POST.get('groups'))
        self.object.save()
        return redirect('users:user')


class RoleUserListView(ListView):
    template_name = 'users/role.html'
    queryset = Group.objects.all().order_by('-pk')


class RoleUserCreateView(CreateView):
    template_name = 'users/add_role.html'
    model = Group
    form_class = RoleUser
    success_url = reverse_lazy('users:roles')


class RoleUserUpdateView(UpdateView):
    template_name = 'users/update_role.html'
    model = Group
    form_class = RoleUser
    success_url = reverse_lazy('users:roles')
