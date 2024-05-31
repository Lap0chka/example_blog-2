from django.contrib.auth.models import User
from django.db import models
import os
from django.db.models.signals import post_save
from django.dispatch import receiver


def user_directory_path(instance, filename):
    return os.path.join(instance.user.username, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_directory_path, blank=True, null=True)
    is_email_verification = models.BooleanField(default=False)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Method to generate profile when user is created"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Method to update profile when user is updated"""
    instance.profile.save()
