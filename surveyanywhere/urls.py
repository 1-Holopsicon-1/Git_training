"""surveyanywhere URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from accounts.views import authentication, register, deauthentication, restore_access, restore_access_check, \
    restore_access_main, registerConfirm, sendEmail, acception, userInfo, changePassword
from main.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='main'),
    path('accounts/login/', authentication, name='user_login'),
    path('accounts/logout/', deauthentication, name='user_logout'),
    path('accounts/register/', register, name='user_register'),
    path('accounts/register_email_confirm/', sendEmail, name='user_register_email_confirm'),
    path('accounts/register_confirm/', registerConfirm, name='user_register_confirm'),
    path('accounts/restore/', restore_access, name='user_restore'),
    path('accounts/restore_confirm/', restore_access_check, name='user_restore_confirm'),
    path('accounts/restore_main/', restore_access_main, name='user_restore_main'),
    path('accounts/', userInfo, name='user_info'),
    path('accounts/change', changePassword, name='user_change'),
]
