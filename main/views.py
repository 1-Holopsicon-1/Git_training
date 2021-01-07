from django.shortcuts import render

from accounts.models import UserProperties
from surveys.models import Survey, SurveyAnswer, SurveyQuestion


def index(request):
    context = {}
    if request.user.is_authenticated:
        context['userProperties'] = UserProperties.objects.get(user=request.user)
        surveys = Survey.objects.filter(isLocked=False).order_by('-rating', '-creationTime', 'title')[:5]
        context['topSurveys'] = []
        for survey in surveys:
            participants = set()
            for question in SurveyQuestion.objects.filter(survey=survey):
                for answer in SurveyAnswer.objects.filter(surveyQuestion=question):
                    for user in answer.users.all():
                        participants.add(user)
            context['topSurveys'].append([survey, len(participants)])
    return render(request, 'index.html', context)