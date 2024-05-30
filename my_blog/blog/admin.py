from django.contrib import admin
from .models import Comments, Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'published']
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Comments)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['body']
