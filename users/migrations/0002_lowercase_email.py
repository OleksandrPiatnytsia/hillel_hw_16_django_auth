from django.db import migrations, models
from django.db.models.functions import Lower


def lowercase_emails(apps, schema_editor):
    """Bring existing emails to lowercase before the constraint is added.

    Otherwise adding the CheckConstraint fails on the first "Ann@Mail.com".
    apps.get_model() returns the historical model (as of this migration),
    not users.models.User — so our save() is not involved here.
    """
    User = apps.get_model("users", "User")
    User.objects.exclude(email=Lower("email")).update(email=Lower("email"))


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        # Reverse: nothing to undo — lowercase emails stay valid
        migrations.RunPython(lowercase_emails, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                error_messages={"unique": "A user with this email already exists."},
                max_length=254,
                unique=True,
                verbose_name="email address",
            ),
        ),
        migrations.AddConstraint(
            model_name="user",
            constraint=models.CheckConstraint(
                condition=models.Q(("email", Lower("email"))),
                name="users_user_email_lowercase",
            ),
        ),
    ]
