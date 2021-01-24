from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from accounts.decorators import ban_check
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

@login_required(login_url='user_login')
@ban_check(redirect_html='permissionError.html', parameters_permanent={'code': 3}, parameters_temporary={'code': 2})
def surveys(request):
    context = {}
    if request.user.is_authenticated:
        context['userProperties'] = UserProperties.objects.get(user=request.user)
        surveys = Survey.objects.filter(isLocked=False).order_by('-rating', '-participants', '-creationTime', 'title')
        context['surveys'] = []
        for survey in surveys:
            context['surveys'].append([survey, survey.participants])
    return render(request, 'surveys.html', context)


def faq(request):
    context = {}
    return render(request, "faq.html", context)


