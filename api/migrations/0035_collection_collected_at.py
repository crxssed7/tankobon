# Generated by Django 4.1.7 on 2023-03-01 18:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0034_historicalvolume_isbn_historicalvolume_page_count_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="collection",
            name="collected_at",
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
