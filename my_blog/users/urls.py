from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'user'


urlpatterns = [
    path('login/', views.LoginMyView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),

]
