# Generated by Django 4.2.5 on 2024-02-27 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("file_manager", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="file",
            name="text_file_path",
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
