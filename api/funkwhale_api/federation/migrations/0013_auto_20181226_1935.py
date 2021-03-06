# Generated by Django 2.0.9 on 2018-12-26 19:35

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [("federation", "0012_auto_20180920_1803")]

    operations = [
        migrations.AlterField(
            model_name="actor",
            name="private_key",
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
        migrations.AlterField(
            model_name="actor",
            name="public_key",
            field=models.TextField(blank=True, max_length=5000, null=True),
        ),
    ]
