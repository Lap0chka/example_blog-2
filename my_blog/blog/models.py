from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from taggit.managers import TaggableManager
from django.utils import timezone


class Post(models.Model):
    """Post model"""

    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=64)
    slug = models.SlugField()
    body = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    published = models.DateTimeField(default=timezone.now)
    tags = TaggableManager()
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    def upload_to(self, filename):
        return f'{self.title}/{filename}'

    image = models.ImageField(upload_to=upload_to, null=True, blank=True)

    class Meta:
        ordering = ['-published']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post', args=[self.slug])

    def count_comments(self):
        comment_count_post = Comments.objects.filter(post=self).count()
        return comment_count_post


class Comments(models.Model):
    """Comments model"""
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
