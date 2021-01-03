from django.shortcuts import render

from accounts.models import UserProperties
from surveys.models import Survey


def index(request):
    context = {}
    if request.user.is_authenticated:
        context['userProperties'] = UserProperties.objects.get(user=request.user)
        context['topSurveys'] = Survey.objects.filter(isLocked=False).order_by('-creationTime', 'title')[:5]
    return render(request, 'index.html', context)