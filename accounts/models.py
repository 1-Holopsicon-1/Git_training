from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProperties(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    email_key_restoration = models.IntegerField(default=0)
    email_key_verification = models.IntegerField(default=0)
    password_restore_called = models.DateTimeField(default=timezone.now)
    email_confirm_called = models.DateTimeField(default=timezone.now)
    email_verified = models.BooleanField(default=False)
    access_limited = models.DateTimeField(default=timezone.now)
    banned = models.DateTimeField(default=timezone.now)
    permanent_ban = models.BooleanField(default=False)

class Complaint(models.Model):
    user = models.ForeignKey(to=User, related_name="user", on_delete=models.CASCADE)
    author = models.ForeignKey(to=User, related_name="author", null=True, on_delete=models.SET_NULL)
    date = models.DateField(default=timezone.now)
    title = models.CharField(default="", max_length=255)
    description = models.CharField(default="", max_length=255)