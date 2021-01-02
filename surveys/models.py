from django.contrib.auth.models import User
from django.db import models

class Survey(models.Model):
    title = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=1000, default='')
    url = models.CharField(max_length=100, default='')
    isLocked = models.BooleanField(default=False)
    creator = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, default=None)

class SurveyQuestion(models.Model):
    multipleChoice = models.BooleanField(default=False)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, default=None)
    text = models.CharField(max_length=255, default='')

class SurveyAnswer(models.Model):
    surveyQuestion = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, default=None)
    users = models.ManyToManyField(User)
    text = models.CharField(max_length=255, default='')