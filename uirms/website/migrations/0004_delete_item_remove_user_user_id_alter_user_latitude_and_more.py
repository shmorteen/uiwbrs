# Generated by Django 4.2.7 on 2024-01-06 08:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0003_user_delete_item"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="user_id",
        ),
        migrations.AlterField(
            model_name="user",
            name="latitude",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="user",
            name="longitude",
            field=models.FloatField(),
        ),
    ]
