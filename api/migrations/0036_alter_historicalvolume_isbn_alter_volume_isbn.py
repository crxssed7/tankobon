# Generated by Django 4.1.7 on 2023-03-04 11:55

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0035_collection_collected_at"),
    ]

    operations = [
        migrations.AlterField(
            model_name="historicalvolume",
            name="isbn",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=20,
                null=True,
                validators=[api.validators.isbn_validator],
            ),
        ),
        migrations.AlterField(
            model_name="volume",
            name="isbn",
            field=models.CharField(
                blank=True,
                max_length=20,
                null=True,
                unique=True,
                validators=[api.validators.isbn_validator],
            ),
        ),
    ]