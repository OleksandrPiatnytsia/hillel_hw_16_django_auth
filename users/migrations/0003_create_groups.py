from django.contrib.auth.management import create_permissions
from django.db import migrations

# Group name -> permission codenames (all from the "books" app).
# Kept here, not imported from app code: a migration must keep working
# the same way even if the app code changes later.
VIEW = ["view_book", "view_author", "view_category"]
EDIT = [
    "add_book",
    "change_book",
    "add_author",
    "change_author",
    # Book categories are saved through BookCategory (ManyToMany through model)
    "view_bookcategory",
    "add_bookcategory",
    "change_bookcategory",
    "delete_bookcategory",
]
MANAGE = [
    "delete_book",
    "delete_author",
    "add_category",
    "change_category",
    "delete_category",
    "manage_stock",  # custom permission from Book.Meta.permissions
]

GROUPS = {
    # Every new user (see SignUpView). Read-only for now; orders etc. later
    "Customers": VIEW,
    # Catalog content: add / edit books and authors, but no deleting and no stock
    "Editors": VIEW + EDIT,
    # Everything editors can + deleting, categories and stock
    "Managers": VIEW + EDIT + MANAGE,
}


def create_groups(apps, schema_editor):
    # Permissions are normally created by the post_migrate signal — that is,
    # AFTER all migrations. On a fresh database they don't exist yet at this
    # point, so create them now. Uses the historical app config, so the
    # permissions match the models as of this migration.
    books_config = apps.get_app_config("books")
    books_config.models_module = True  # create_permissions() skips apps without it
    create_permissions(books_config, apps=apps, verbosity=0)
    books_config.models_module = None

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")
    for name, codenames in GROUPS.items():
        group, _ = Group.objects.get_or_create(name=name)
        permissions = Permission.objects.filter(
            content_type__app_label="books", codename__in=codenames
        )
        # Fail loudly on a typo instead of creating a group with fewer rights
        missing = set(codenames) - set(permissions.values_list("codename", flat=True))
        if missing:
            raise RuntimeError(f"Unknown permissions for {name}: {sorted(missing)}")
        # set(): safe to re-run, the group gets exactly this list
        group.permissions.set(permissions)


def delete_groups(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name__in=GROUPS).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_lowercase_email"),
        ("books", "0007_book_manage_stock_permission"),
        ("auth", "0012_alter_user_first_name_max_length"),
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.RunPython(create_groups, delete_groups),
    ]
