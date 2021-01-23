from django.contrib import messages
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RegistrationForm:
    error_messages = {
        'username_error': 'Username is incorrect or empty',
        'username_busy': 'User with such username already exists',
        'email_error': 'Email is incorrect or empty',
        'email_busy': 'User with such email already exists',
        'password_error': 'Password is incorrect or empty',
        'password_mismatch': 'The two passwords do not match',
        'name_error': 'First and last names may be empty or contain only letters',
    }

    def __init__(self, request=None):
        self.check = (request is not None)
        self.data = {}
        self.request = request
        if self.check:
            self.data['username'] = request.POST.get('username', None)
            self.data['email'] = request.POST.get('email', None)
            self.data['first_name'] = request.POST.get('first_name', '')
            self.data['last_name'] = request.POST.get('last_name', '')
            self.data['password1'] = request.POST.get('password1', None)
            self.data['password2'] = request.POST.get('password2', None)

    def is_valid(self, send_errors=True):
        errors = []
        if not self.check:
            return False

        if self.data['username'] is None or not self.data['username']:
            errors.append(self.error_messages['username_error'])
        else:
            try:
                User.objects.get(username=self.data['username'])
            except:
                pass
            else:
                errors.append(self.error_messages['username_busy'])

        if not self.email_check(self.data['email']):
            errors.append(self.error_messages['email_error'])
        else:
            try:
                User.objects.get(email=self.data['email'])
            except:
                pass
            else:
                errors.append(self.error_messages['email_busy'])

        if self.data['password1'] != self.data['password2']:
            errors.append(self.error_messages['password_mismatch'])
        elif self.data['password1'] is None or not self.data['password1']:
            errors.append(self.error_messages['password_error'])
        else:
            try:
                password_validation.validate_password(self.data['password1'])
            except ValidationError as v_errors:
                for error in v_errors:
                    errors.append(error)

        if (self.data['first_name'] != '' and not self.data['first_name'].isalpha()) or \
            (self.data['last_name'] != '' and not self.data['last_name'].isalpha()):
            errors.append(self.error_messages['name_error'])

        if len(errors) > 0:
            if send_errors:
                for error in errors:
                    messages.error(self.request, error)
            return False
        return True

    def save(self):
        if self.is_valid(send_errors=False):
            User.objects.create_user(self.data['username'], self.data['email'], self.data['password1'],
                                     first_name=self.data['first_name'],
                                     last_name=self.data['last_name'])

    def email_check(self, email: str):
        if email is None:
            return False
        if email.count('@') != 1:
            return False
        if email.index('@') == 0:
            return False
        if email.count('.', email.index('@')) != 1:
            return False
        if email[-1] == '.':
            return False
        if email.index('.', email.index('@')) - email.index('@') == 1:
            return False
        return True

class PasswordResetForm:
    error_messages = {
        'password_old_error': 'Old password is incorrect',
        'password_error': 'Password is incorrect or empty',
        'password_mismatch': 'The two passwords do not match',
        'password_collision': 'New password is the same as the old one',
    }

    def __init__(self, request=None):
        self.check = (request is not None)
        self.data = {}
        self.request = request
        if self.check:
            self.data['old_password'] = request.POST.get('old_password', '')
            self.data['password1'] = request.POST.get('password1', None)
            self.data['password2'] = request.POST.get('password2', None)

    def is_valid(self, send_errors=True):
        errors = []
        if not self.check:
            return False

        user = None
        try:
            user = User.objects.get(username=self.request.user.username)
        except:
            return False

        if self.data['password1'] != self.data['password2']:
            errors.append(self.error_messages['password_mismatch'])
        elif self.data['password1'] is None or not self.data['password1']:
            errors.append(self.error_messages['password_error'])
        else:
            try:
                password_validation.validate_password(self.data['password1'])
            except ValidationError as v_errors:
                for error in v_errors:
                    errors.append(error)
            else:
                if not check_password(self.data['old_password'], user.password):
                    errors.append(self.error_messages['password_old_error'])
                elif self.data['old_password'] == self.data['password1']:
                    errors.append(self.error_messages['password_collision'])

        if len(errors) > 0:
            if send_errors:
                for error in errors:
                    messages.error(self.request, error)
            return False
        return True

    def save(self):
        if self.is_valid(send_errors=False):
            user = User.objects.get(username=self.request.user.username)
            user.set_password(self.data['password1'])

            user.save()

    def email_check(self, email: str):
        if email is None:
            return False
        if email.count('@') != 1:
            return False
        if email.index('@') == 0:
            return False
        if email.count('.', email.index('@')) != 1:
            return False
        if email[-1] == '.':
            return False
        if email.index('.', email.index('@')) - email.index('@') == 1:
            return False
        return True

