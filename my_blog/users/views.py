import uuid
from django.contrib.auth.decorators import login_required
from .forms import RegisterUserForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, reverse
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from .tasks import send_email_verification
from .forms import UserProfileForm
from .models import Profile
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User


class LoginMyView(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('user:profile', args=[user_id])


class RegisterUser(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterUserForm

    def get_success_url(self):
        return reverse('user:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have registered successfully. Please log in.')
        name = form.cleaned_data['username']
        email = form.cleaned_data['email']
        token = uuid.uuid4().hex
        base_url = self.request.build_absolute_uri(reverse_lazy('user:confirm_email', args=[token]))
        send_email_verification.delay(name, email, base_url, token)
        return response


def confirm_email(reqeust, token):
    redis_key = settings.MYVARRIABLE_USER_CONFIRMATION_KEY.format(token=token)
    user_info = cache.get(redis_key) or {}

    if user_info:
        username = user_info.get("user_name")
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        profile.is_email_verification = True
        profile.save()
        return redirect(to=reverse_lazy('blog:index'))
    else:
        return redirect(to=reverse_lazy('user:login'))


class UserProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'users/profile.html'

    def get_success_url(self):
        user_id = self.request.user.id
        return reverse('user:profile', args=[user_id])

    def get_object(self, queryset=None):
        return self.request.user
