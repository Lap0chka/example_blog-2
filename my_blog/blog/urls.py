from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='index'),
    path('post/<str:slug>', views.singel_post, name='post'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
