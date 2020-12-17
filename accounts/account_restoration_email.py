def get_email_body(username, code):
    return f'''Dear {username},
If you see this message it means that you or somebody else tried to restore password for your account on SurveyAnyWhere. If you did not do it, please, ignore this message for security reasons.

If you want to change your password, type in the password reset confirmation tab these numbers:
{code}

This letter was generated automatically. Please, do not reply on it.

With best wishes,
Support Team of SurveyAnyWhere'''