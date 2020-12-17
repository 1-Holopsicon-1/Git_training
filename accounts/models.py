from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class UserProperties(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    email_key = models.IntegerField()
    password_restore_called = models.DateTimeField(default=timezone.now)