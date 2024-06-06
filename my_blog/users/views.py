import uuid
from .forms import RegisterUserForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect, reverse, render
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView, UpdateView
from .tasks import send_email_verification
from .forms import UserProfileForm, AddPostForm
from .models import Profile
from django.conf import settings
from django.core.cache import cache
from django.contrib.auth.models import User
from blog.models import Post


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
        send_user_email(self.request)
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
        messages.success(reqeust, 'You have confirm your email successfully.')
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

    def form_valid(self, form):
        user = self.request.user
        if form.cleaned_data['email'] != user.email:
            send_user_email(self.request)
        response = super().form_valid(form)
        image = form.cleaned_data['image']
        profile = Profile.objects.get(user=user)
        profile.image = image
        profile.save()
        return response

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.objects.get(user=user)
        form = UserProfileForm(instance=user)
        print(profile.image)
        return render(request, 'users/profile.html', {'profile': profile, 'form': form})


def send_user_email(request):
    user = request.user
    token = uuid.uuid4().hex
    base_url = request.build_absolute_uri(reverse_lazy('user:confirm_email', args=[token]))
    send_email_verification.delay(user.username, user.email, base_url, token)
    message = 'Email has been sent successfully'
    if user.is_authenticated:
        messages.success(request, message)
        return redirect(reverse_lazy('user:profile', args=[user.id]))
    messages.success(request, message)
    return redirect(reverse_lazy('blog:index'))


class AddPostView(CreateView):
    template_name = 'users/add_post.html'
    form_class = AddPostForm
    model = Post

    def get_success_url(self):
        messages.success(self.request, "We got your post. Soon we'll check it and add\nThank you")
        return reverse('user:add_post')

    def form_valid(self, form):
        user = self.request.user
        post = form.save(commit=False)
        post.author = user
        response = super().form_valid(form)
        return response
