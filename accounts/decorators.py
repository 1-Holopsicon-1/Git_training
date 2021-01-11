from django.contrib import messages as messages_module
from django.contrib.auth import REDIRECT_FIELD_NAME, logout
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone

from accounts.models import UserProperties


def staff_required(redirect_html, parameters=dict()):
    """
    Decorator for views that checks that the user is staff,
    redirecting to the error HTML-page if necessary.
    """
    def decorator(view_function=None):
        def wrapper(request, *args, **kwargs):
            if request.user.is_staff:
                return view_function(request, *args, **kwargs)
            else:
                return render(request, redirect_html, parameters)

        return wrapper

    return decorator


def email_verified(redirect_url=None, messages=[], customCheck=None):
    """
    Decorator for views that checks that the user's email is confirmed,
    redirecting to another page if necessary.
    """
    def defaultCheck(user):
        return UserProperties.objects.get(user=user).email_verified

    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            if customCheck != None:
                check = customCheck
            else:
                check = defaultCheck
            if check(request.user):
                return view_function(request, *args, **kwargs)
            else:
                for message in messages:
                    messages_module.error(request, message)

                url = redirect_url
                if url is None:
                    url = reverse('user_info') + f'?user={request.user.username}'
                return redirect(url)

        return wrapper

    return decorator


def limits_check(redirect_html, parameters=dict(), customCheck=None):
    """
    Decorator for views that checks that the user is not limited in rights,
    redirecting to error HTML-page if necessary.
    """
    def defaultCheck(user):
        return (timezone.now() - UserProperties.objects.get(user=user).access_limited).total_seconds() > 0

    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            if customCheck != None:
                check = customCheck
            else:
                check = defaultCheck
            if check(request.user):
                return view_function(request, *args, **kwargs)
            else:
                return render(request, redirect_html, parameters)

        return wrapper

    return decorator


def ban_check(redirect_html, parameters_temporary=dict(), parameters_permanent=dict(), customCheck=None):
    """
    Decorator for views that checks that the user is not banned,
    redirecting to error HTML-page if necessary.
    """
    def defaultCheck(user):
        if not user.is_authenticated:
            return 0
        if UserProperties.objects.get(user=user).permanent_ban:
            return 2
        if (timezone.now() - UserProperties.objects.get(user=user).banned).total_seconds() > 0:
            return 0
        return 1

    def decorator(view_function):
        def wrapper(request, *args, **kwargs):
            if customCheck != None:
                check = customCheck
            else:
                check = defaultCheck
            if check(request.user) == 0:
                return view_function(request, *args, **kwargs)
            elif check(request.user) == 1:
                parameters_temporary['blockEnd'] = UserProperties.objects.get(user=request.user).banned
                logout(request)
                return render(request, redirect_html, parameters_temporary)
            else:
                logout(request)
                return render(request, redirect_html, parameters_permanent)

        return wrapper

    return decorator
