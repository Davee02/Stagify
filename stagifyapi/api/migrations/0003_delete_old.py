# Generated by Django 3.1.3 on 2020-12-10 14:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_concert"),
    ]

    operations = [
        migrations.DeleteModel(
            name="Choice",
        ),
        migrations.DeleteModel(
            name="Question",
        ),
    ]
