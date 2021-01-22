from django.shortcuts import render

from accounts.models import UserProperties
from surveys.models import Survey, SurveyAnswer, SurveyQuestion


def index(request):
    context = {}
    if request.user.is_authenticated:
        context['userProperties'] = UserProperties.objects.get(user=request.user)
        context['is_staff'] = request.user.is_staff
        surveys = Survey.objects.filter(isLocked=False).order_by('-rating', '-participants', '-creationTime', 'title')[:5]
        context['topSurveys'] = []
        for survey in surveys:
            context['topSurveys'].append([survey, survey.participants])
    return render(request, 'index.html', context)