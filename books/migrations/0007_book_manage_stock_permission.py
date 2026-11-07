from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("books", "0006_remove_book_author_name_alter_book_author"),
    ]

    operations = [
        # Meta.permissions is stored in the migration state; the Permission
        # row itself is created by create_permissions() (post_migrate signal
        # or the users.0003 data migration)
        migrations.AlterModelOptions(
            name="book",
            options={
                "ordering": ["title"],
                "permissions": [("manage_stock", "Can change stock quantity")],
            },
        ),
    ]
