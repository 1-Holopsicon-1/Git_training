from django.contrib import admin

from surveys.models import SurveyAnswer, Survey

admin.site.register(Survey)
admin.site.register(SurveyAnswer)