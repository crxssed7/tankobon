# Generated by Django 3.2.7 on 2022-04-10 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="manga",
            name="status",
            field=models.CharField(
                choices=[
                    ("RELEASING", "Releasing"),
                    ("FINISHED", "Finished"),
                    ("PLANNED", "Planned"),
                ],
                max_length=15,
            ),
        ),
    ]
