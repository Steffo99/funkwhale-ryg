# Generated by Django 2.2.3 on 2019-08-01 08:34

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("federation", "0020_auto_20190730_0846"),
        ("moderation", "0002_auto_20190213_0927"),
    ]

    operations = [
        migrations.CreateModel(
            name="Report",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("fid", models.URLField(db_index=True, max_length=500, unique=True)),
                ("url", models.URLField(blank=True, max_length=500, null=True)),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                (
                    "creation_date",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("summary", models.TextField(max_length=50000, null=True)),
                ("handled_date", models.DateTimeField(null=True)),
                ("is_handled", models.BooleanField(default=False)),
                (
                    "type",
                    models.CharField(
                        choices=[
                            ("takedown_request", "Takedown request"),
                            ("invalid_metadata", "Invalid metadata"),
                            ("illegal_content", "Illegal content"),
                            ("offensive_content", "Offensive content"),
                            ("other", "Other"),
                        ],
                        max_length=40,
                    ),
                ),
                ("submitter_email", models.EmailField(max_length=254, null=True)),
                ("target_id", models.IntegerField(null=True)),
                (
                    "target_state",
                    django.contrib.postgres.fields.jsonb.JSONField(null=True),
                ),
                (
                    "submitter",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="reports",
                        to="federation.Actor",
                    ),
                ),
                (
                    "assigned_to",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="assigned_reports",
                        to="federation.Actor",
                    ),
                ),
                (
                    "target_content_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "target_owner",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="federation.Actor",
                    ),
                ),
            ],
            options={"abstract": False},
        )
    ]
