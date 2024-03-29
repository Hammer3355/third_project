# Generated by Django 4.2 on 2024-03-13 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo",
            name="important",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="todo",
            name="date_completed",
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
