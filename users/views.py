from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, resolve_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.generic import CreateView

from .forms import LoginForm, SignUpForm


class UserLoginView(SuccessMessageMixin, LoginView):
    """Login page.

    LoginView itself: validates the form, calls login() (creates the
    session) and redirects to ?next=... or to LOGIN_REDIRECT_URL.
    """

    template_name = "users/auth_form.html"
    form_class = LoginForm
    # A logged-in user who opens /accounts/login/ is sent away right away
    redirect_authenticated_user = True
    success_message = "Welcome back, %(username)s!"
    extra_context = {"title": "Log in", "submit_label": "Log in"}


class UserLogoutView(LogoutView):
    """Logout: POST only (Django 5+), then redirect to LOGOUT_REDIRECT_URL."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Added after logout(): the session is already flushed, but the
        # message storage still works for this response
        messages.info(request, "You have been logged out.")
        return response


class SignUpView(SuccessMessageMixin, CreateView):
    """Registration + automatic login of the new user."""

    form_class = SignUpForm
    template_name = "users/auth_form.html"
    success_message = "Account created. Welcome, %(username)s!"
    extra_context = {"title": "Sign up", "submit_label": "Create account"}

    def dispatch(self, request, *args, **kwargs):
        # Same as redirect_authenticated_user in LoginView
        if request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        # super() saves the user (self.object) and returns the redirect
        response = super().form_valid(form)
        # Log in right away, so the user doesn't type the password twice
        login(self.request, self.object)
        return response

    def get_success_url(self):
        # Like LoginView: go back to ?next=... if it points to our site.
        # The check protects from "open redirect" to another domain.
        next_url = self.request.POST.get("next") or self.request.GET.get("next")
        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={self.request.get_host()},
            require_https=self.request.is_secure(),
        ):
            return next_url
        return resolve_url(settings.LOGIN_REDIRECT_URL)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # LoginView puts "next" into context itself; do the same here so
        # the shared template keeps it in a hidden field
        context["next"] = self.request.GET.get("next", "")
        return context
