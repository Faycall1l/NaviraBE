# Generated by Django 5.0.4 on 2024-04-26 23:43

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("ship_quay_api", "0002_remove_quay_tools_remove_ship_arrival_time_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="quay",
            name="tools",
            field=models.TextField(blank=True),
        ),
    ]