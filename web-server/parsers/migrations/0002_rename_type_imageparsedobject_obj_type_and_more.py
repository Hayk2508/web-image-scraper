# Generated by Django 5.0.6 on 2024-06-11 09:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("parsers", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="imageparsedobject",
            old_name="type",
            new_name="obj_type",
        ),
        migrations.RenameField(
            model_name="videoparsedobject",
            old_name="type",
            new_name="obj_type",
        ),
    ]