from django.contrib.auth.models import User
from django.db import models
import os


def user_directory_path(instance, filename):
    return os.path.join(instance.user.username, filename)


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    is_email_verification = models.BooleanField(default=False)

