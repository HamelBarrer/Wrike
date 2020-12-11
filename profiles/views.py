from django.shortcuts import redirect, render
from django.contrib import messages
from django.views.generic import UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from users.forms import UserUpdateForm

from .forms import ProfileForm
from .models import Profile


@login_required(login_url='users:login')
def profile_view(request):
    template_name = 'profiles/profil.html'

    user = request.user
    profile = Profile.objects.filter(user=user).first()

    return render(request, template_name, {
        'profile': profile,
    })


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    success_url = 'users:login'
    template_name = 'profiles/update_profile.html'
    form_class = ProfileForm
    model = Profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.method == 'POST':
            context['form_user'] = UserUpdateForm(
                self.request.POST, instance=self.request.user)
        else:
            context['form_user'] = UserUpdateForm(instance=self.request.user)

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        form_user = context['form_user']

        self.object = form.save()
        form_user.save()

        return redirect('profiles:profile')
