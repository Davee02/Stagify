# Generated by Django 3.1.3 on 2020-12-10 14:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0004_create_artist"),
    ]

    operations = [
        migrations.AddField(
            model_name="concert",
            name="artist",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.DO_NOTHING, to="api.artist"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="concert",
            name="duration",
            field=models.PositiveIntegerField(),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="concert",
            name="startDateTime",
            field=models.DateTimeField(),
            preserve_default=False,
        ),
    ]
