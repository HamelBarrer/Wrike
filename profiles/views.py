from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.urls import reverse_lazy

from users.forms import UserForm
from users.models import User

from .forms import ProfileForm
from .models import Profile


class ProfileTemplateView(TemplateView):
    template_name = 'profiles/profil.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile'] = Profile.objects.get(user=self.request.user)

        return context


class ProfileUpdateView(UpdateView):
    template_name = 'profiles/update_profile.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profiles:profile')

    def get_context_data(self, **kwargs):
        user = User.objects.get(pk=self.request.user.pk)
        context = super().get_context_data(**kwargs)
        context['form_user'] = UserForm(instance=user)

        return context
