# Generated by Django 3.2.7 on 2022-04-12 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0013_manga_fandom"),
    ]

    operations = [
        migrations.AlterField(
            model_name="manga",
            name="anilist_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="manga",
            name="anime_planet_slug",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="manga",
            name="kitsu_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="manga",
            name="mal_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="manga",
            name="mangaupdates_id",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
