# Generated by Django 2.0.3 on 2018-05-15 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("music", "0026_trackfile_accessed_date")]

    operations = [
        migrations.AddField(
            model_name="trackfile",
            name="bitrate",
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="trackfile",
            name="size",
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
