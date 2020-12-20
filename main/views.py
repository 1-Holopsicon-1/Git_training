from django.shortcuts import render

from accounts.models import UserProperties


def index(request):
    context = {}
    if request.user.is_authenticated:
        context['userProperties'] = UserProperties.objects.get(user=request.user)
    return render(request, 'index.html', context)