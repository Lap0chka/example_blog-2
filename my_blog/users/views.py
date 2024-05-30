from .forms import RegisterUserForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import CreateView


class LoginMyView(LoginView):
    template_name = "users/login.html"

    def get_success_url(self):
        return reverse_lazy('blog:index')


class RegisterUser(CreateView):
    template_name = 'users/register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('user:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'You have registered successfully. Please log in.')
        return response
