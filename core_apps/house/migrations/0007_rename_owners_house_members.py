# Generated by Django 4.2.5 on 2024-02-03 03:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("house", "0006_alter_room_description"),
    ]

    operations = [
        migrations.RenameField(
            model_name="house",
            old_name="owners",
            new_name="members",
        ),
    ]