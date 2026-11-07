from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "users"

    def ready(self):
        # Importing the module runs the @receiver decorators, which connect
        # the signal handlers. ready() runs once, after all apps are loaded.
        from . import signals  # noqa: F401
