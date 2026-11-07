from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from .models import User


class BootstrapFormMixin:
    """Adds Bootstrap's "form-control" class to every field widget.

    The auth forms come from Django, so we can't list widgets in Meta like
    in BookForm — instead the classes are added after the fields are built.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class LoginForm(BootstrapFormMixin, AuthenticationForm):
    """Login by username + password (Django's AuthenticationForm)."""


class SignUpForm(BootstrapFormMixin, UserCreationForm):
    """Registration: username, email, password + confirmation.

    UserCreationForm already does the important parts: checks that the two
    passwords match, runs AUTH_PASSWORD_VALIDATORS, rejects a username that
    differs only by case, and saves the password as a hash (set_password).

    No clean_email() needed: User.clean() lowercases the email before the
    unique check, so "Ann@Mail.com" is caught as a duplicate of "ann@mail.com"
    (error text comes from error_messages on the model field).
    """

    class Meta(UserCreationForm.Meta):
        # The parent Meta points to the built-in auth.User; our model
        # replaced it (AUTH_USER_MODEL), so the form must use users.User
        model = User
        fields = ("username", "email")
