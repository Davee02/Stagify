# Generated by Django 3.1.3 on 2020-12-20 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_artist_userid"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="concert",
            name="state",
        ),
    ]
