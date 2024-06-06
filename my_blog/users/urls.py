from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'user'


urlpatterns = [
    path('login/', views.LoginMyView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('profile/<int:id>', views.UserProfileView.as_view(), name='profile'),
    path('add_post/', views.AddPostView.as_view(), name='add_post'),
    path('send_email/', views.send_user_email, name='send_email'),
    path('confirm_email/<str:token>', views.confirm_email, name='confirm_email'),
]
