# Generated by Django 4.1.4 on 2022-12-11 11:38

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("api", "0021_alter_volume_absolute_number"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalVolume",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                (
                    "absolute_number",
                    models.IntegerField(
                        default=-1,
                        validators=[django.core.validators.MinValueValidator(-1)],
                    ),
                ),
                ("chapters", models.TextField()),
                ("locked", models.BooleanField(default=False)),
                ("poster", models.URLField(blank=True, max_length=750)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "manga",
                    models.ForeignKey(
                        blank=True,
                        db_constraint=False,
                        null=True,
                        on_delete=django.db.models.deletion.DO_NOTHING,
                        related_name="+",
                        to="api.manga",
                    ),
                ),
            ],
            options={
                "verbose_name": "historical volume",
                "verbose_name_plural": "historical volumes",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name="HistoricalManga",
            fields=[
                (
                    "id",
                    models.BigIntegerField(
                        auto_created=True, blank=True, db_index=True, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("romaji", models.CharField(max_length=150)),
                ("description", models.TextField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("RELEASING", "Releasing"),
                            ("FINISHED", "Finished"),
                            ("PLANNED", "Planned"),
                        ],
                        max_length=15,
                    ),
                ),
                ("start_date", models.DateField()),
                ("poster", models.URLField(blank=True, max_length=750)),
                ("banner", models.URLField(blank=True, max_length=750)),
                ("anilist_id", models.PositiveIntegerField(blank=True, null=True)),
                ("mal_id", models.PositiveIntegerField(blank=True, null=True)),
                ("mangaupdates_id", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "anime_planet_slug",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("kitsu_id", models.PositiveIntegerField(blank=True, null=True)),
                ("fandom", models.URLField(blank=True, null=True)),
                ("magazine", models.CharField(blank=True, max_length=150, null=True)),
                ("volume_count", models.PositiveIntegerField(default=1)),
                ("locked", models.BooleanField(default=False)),
                ("last_updated", models.DateTimeField(blank=True, editable=False)),
                ("history_id", models.AutoField(primary_key=True, serialize=False)),
                ("history_date", models.DateTimeField(db_index=True)),
                ("history_change_reason", models.CharField(max_length=100, null=True)),
                (
                    "history_type",
                    models.CharField(
                        choices=[("+", "Created"), ("~", "Changed"), ("-", "Deleted")],
                        max_length=1,
                    ),
                ),
                (
                    "history_user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="+",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "historical manga",
                "verbose_name_plural": "historical mangas",
                "ordering": ("-history_date", "-history_id"),
                "get_latest_by": ("history_date", "history_id"),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
