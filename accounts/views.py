from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from accounts.forms import RegistrationForm


def register(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account with username {username} created.')

    context = {'form': form}
    return render(request, 'signup.html', context)

def authentication(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password incorrect')

    context = {}
    return render(request, 'signin.html', context)

def deauthentication(request):
    logout(request)
    return redirect('/')