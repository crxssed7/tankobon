# Generated by Django 3.2.7 on 2022-04-10 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20220410_1616'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='anime_planet_slug',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='manga',
            name='kitsu_id',
            field=models.PositiveIntegerField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='manga',
            name='mangaupdates_id',
            field=models.PositiveIntegerField(blank=True, default=1),
            preserve_default=False,
        ),
    ]
