from random import randint
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.forms import SetPasswordForm, PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.template.defaulttags import url
from django.urls import reverse
from django.utils import timezone

from accounts.emailing import get_confirm_email_body, get_password_email_body
from accounts.forms import RegistrationForm
from accounts.models import UserProperties
from surveyanywhere.settings import EMAIL_HOST_USER

#<editor-fold desc="MAIN PART">
def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('main'))

    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                user = None

            if user is None:
                form.save()
                username = form.cleaned_data.get('username')
                userParams = UserProperties(user=User.objects.get(username=username))
                userParams.save()
                messages.info(request, f'Account with username {username} created.')
                return redirect(reverse('user_login'))
            else:
                messages.error(request, f'Account with email "{email}" already exists.')

    context = {'form': form}
    return render(request, 'signup.html', context)

def sendEmail(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('main'))
    userProp = UserProperties.objects.get(user=user)
    number = randint(100000, 999999)
    email = EmailMessage(
        'Account email verification',
        get_confirm_email_body(user.username, number),
        EMAIL_HOST_USER,
        [user.email],
    )
    email.send()
    userProp.email_key_verification = number
    userProp.email_confirm_called = timezone.now()
    userProp.save()
    return redirect(reverse('user_register_confirm'))

def registerConfirm(request):
    user = request.user
    if not user.is_authenticated:
        return redirect(reverse('main'))

    userProp = UserProperties.objects.get(user=user)
    value = userProp.email_key_verification
    if value == 0 or (timezone.now() - userProp.password_restore_called).total_seconds() > 1800:
        userProp.email_key_restoration = 0
        userProp.save()
        return redirect(reverse('main'))

    if request.method == "POST":
        digit = request.POST.get('Digit1')
        digit += request.POST.get('Digit2')
        digit += request.POST.get('Digit3')
        digit += request.POST.get('Digit4')
        digit += request.POST.get('Digit5')
        digit += request.POST.get('Digit6')

        if int(digit) == value:
            userProp.email_key_verification = 0
            userProp.email_verified = True
            userProp.save()
            messages.info(request, f'Email of {user.username} verified.')
            return redirect(reverse('user_login'))
        else:
            messages.error(request, f'Email code incorrect.')
    context = {
        'key': value,
    }
    return render(request, 'signup_confirm.html', context)

def authentication(request):
    '''if not acception(request):
        return redirect(reverse('user_register'))    тут я проверял работоспособность функции'''

    if request.user.is_authenticated:
        return redirect(reverse('main'))

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(reverse('main'))
        else:
            messages.info(request, 'Username or password incorrect')

    context = {}
    return render(request, 'signin.html', context)

def deauthentication(request):
    logout(request)
    return redirect(reverse('main'))
#</editor-fold>

def restore_access(request):
    if request.user.is_authenticated:
        return redirect(reverse('main'))

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')

        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            user = None

        if user is not None and user.email == email:
            number = randint(100000, 999999)
            email = EmailMessage(
                'Account access restoration',
                get_password_email_body(username, number),
                EMAIL_HOST_USER,
                [email],
            )
            email.send()
            userParams = UserProperties.objects.get(user=user)
            userParams.email_key_restoration = number
            userParams.password_restore_called = timezone.now()
            userParams.save()
            return redirect(reverse('user_restore_confirm') + f'?user={username}')
        else:
            messages.info(request, 'Username or email incorrect')

    context = {}
    return render(request, 'restore.html', context)

def restore_access_check(request):
    if request.user.is_authenticated:
        return redirect(reverse('main'))

    username = request.GET.get('user', '')
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect(reverse('main'))

    userProp = UserProperties.objects.get(user=user)
    value = userProp.email_key_restoration
    if value == 0 or (timezone.now() - userProp.password_restore_called).total_seconds() > 1800:
        userProp.email_key_restoration = 0
        userProp.save()
        return redirect(reverse('main'))

    if request.method == "POST":
        digit = request.POST.get('Digit1')
        digit += request.POST.get('Digit2')
        digit += request.POST.get('Digit3')
        digit += request.POST.get('Digit4')
        digit += request.POST.get('Digit5')
        digit += request.POST.get('Digit6')

        if int(digit) == value:
            return redirect(reverse('user_restore_main') + f'?user={username}')
        else:
            messages.error(request, f'Email code incorrect.')
    context = {
        'key': value,
    }
    return render(request, 'restore_check.html', context)

def restore_access_main(request):
    if request.user.is_authenticated:
        return redirect(reverse('main'))

    username = request.GET.get('user', None)
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect(reverse('main'))
    userProp = UserProperties.objects.get(user=user)
    if userProp.email_key_restoration == 0 or (timezone.now() - userProp.password_restore_called).total_seconds() > 1800:
        userProp.email_key_restoration = 0
        userProp.save()
        return redirect(reverse('main'))

    context = {}
    form = SetPasswordForm(user)
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            new_password = request.POST['new_password1']
            if not check_password(new_password, user.password):
                user.set_password(new_password)
                user.save()
                userProp.email_key_restoration = 0
                userProp.save()
                messages.info(request, 'Password was updated')
                return HttpResponseRedirect(reverse('user_login'))
            else:
                messages.error(request, 'New password is the same as the old one')
    context['form'] = form
    return render(request, 'restore_main.html', context)

def changePassword(request):
    if not request.user.is_authenticated:
        return redirect(reverse('main'))

    user = request.user
    context = {}
    form = PasswordChangeForm(user)
    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            new_password = request.POST['new_password1']
            if not check_password(new_password, user.password):
                user.set_password(new_password)
                user.save()
                logout(request)
                messages.info(request, 'Password was updated')
                return HttpResponseRedirect(reverse('user_login'))
            else:
                messages.error(request, 'New password is the same as the old one')
    context['form'] = form

    return render(request, 'password_reset.html', context)

def userInfo(request):
    username = request.GET.get('user', None)
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect(reverse('main'))

    context = {
        'isOwner': False,
        'username': username,
        'userProperties': None,
    }
    if request.user.is_authenticated and request.user.username == username:
        context['isOwner'] = True
        context['userProperties'] = UserProperties.objects.get(user=user)
    return render(request, 'user_page.html', context)

def acception(request):
    user = request.user
    if not user.is_authenticated:
        return 0

    userProp = UserProperties.objects.get(user=user)

    if userProp.rating <= 0 and request.method == "POST":
        return 0
    return 1