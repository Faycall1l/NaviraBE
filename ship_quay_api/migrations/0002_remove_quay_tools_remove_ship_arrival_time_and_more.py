# Generated by Django 5.0.4 on 2024-04-26 23:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ship_quay_api", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="quay",
            name="tools",
        ),
        migrations.RemoveField(
            model_name="ship",
            name="arrival_time",
        ),
        migrations.RemoveField(
            model_name="ship",
            name="assigned_quay",
        ),
        migrations.RemoveField(
            model_name="ship",
            name="departure_time",
        ),
        migrations.RemoveField(
            model_name="ship",
            name="required_tools",
        ),
        migrations.RemoveField(
            model_name="ship",
            name="size",
        ),
        migrations.AddField(
            model_name="ship",
            name="quay",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="ships",
                to="ship_quay_api.quay",
            ),
        ),
        migrations.AlterField(
            model_name="quay",
            name="capacity",
            field=models.IntegerField(default=0),
        ),
    ]
