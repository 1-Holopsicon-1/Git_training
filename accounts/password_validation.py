from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class AlphabeticPasswordValidator:
    """
    Validate whether the password is alphanumeric.
    """
    def validate(self, password, user=None):
        if password.isalpha():
            raise ValidationError(
                _("This password is entirely alphabetic."),
                code='password_entirely_alphabetic',
            )

    def get_help_text(self):
        return _('Your password can’t be entirely  alphabetic.')