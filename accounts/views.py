from random import randint
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.defaulttags import url
from django.urls import reverse

from accounts.account_restoration_email import get_email_body
from accounts.forms import RegistrationForm
from surveyanywhere.settings import EMAIL_HOST_USER


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
                messages.success(request, f'Account with username "{username}" created.')
            else:
                messages.error(request, f'Account with email "{email}" already exists.')

    context = {'form': form}
    return render(request, 'signup.html', context)

def authentication(request):
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
                get_email_body(username, number),
                EMAIL_HOST_USER,
                [email],
            )
            email.send()
            return redirect(reverse('user_restore_confirm') + f'?key={hex(number)[2:]}&user={username}')
        else:
            messages.info(request, 'Username or email incorrect')

    context = {}
    return render(request, 'restore.html', context)

def restore_access_check(request):
    value = int('0x' + request.GET.get('key', '0'), 16)
    username = request.GET.get('user', '')
    if request.method == "POST":
        digit = request.POST.get('Digit1')
        digit += request.POST.get('Digit2')
        digit += request.POST.get('Digit3')
        digit += request.POST.get('Digit4')
        digit += request.POST.get('Digit5')
        digit += request.POST.get('Digit6')

        if int(digit) == value:
            return redirect(reverse('user_restore_main') + f'?user={username}')
    context = {
        'key': value,
    }
    return render(request, 'restore_check.html', context)

def restore_access_main(request):
    username = request.GET.get('user', None)
    try:
        user = User.objects.get(username=username)
    except ObjectDoesNotExist:
        return redirect(reverse('main'))
    form = SetPasswordForm(user)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect(reverse('user_login'))
    context = {}
    return render(request, 'restore_main.html', context)