# Generated by Django 4.2.5 on 2023-12-11 17:29

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("stories", "0007_userstory_alt_text_userstory_caption_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userstory",
            name="caption",
            field=models.CharField(blank=True, max_length=200),
        ),
    ]