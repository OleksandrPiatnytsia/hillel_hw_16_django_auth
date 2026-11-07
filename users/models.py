from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Site user.

    Inherits everything from the built-in user (username, password,
    first/last name, is_staff, groups, user_permissions, ...). Login stays
    by username; the only change is the email field.

    Even without extra fields a custom user model is worth having from the
    very first migration: switching AUTH_USER_MODEL later, when other tables
    already point to auth_user, is a painful manual migration.
    """

    # In AbstractUser email is optional (blank=True) and not unique.
    # Here it is required and unique, so one email = one account.
    email = models.EmailField("email address", unique=True)

    # Extra fields that `createsuperuser` asks for (besides USERNAME_FIELD
    # and password). AbstractUser already has ["email"]; kept explicit.
    REQUIRED_FIELDS = ["email"]

    class Meta(AbstractUser.Meta):
        # AbstractUser.Meta holds verbose_name "user"; inheriting it keeps
        # the admin labels the same as for the built-in model
        pass
