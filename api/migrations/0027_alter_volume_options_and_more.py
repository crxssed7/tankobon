# Generated by Django 4.1.4 on 2022-12-18 10:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0026_alter_edition_unique_together"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="volume",
            options={"ordering": ["absolute_number"]},
        ),
        migrations.RemoveField(
            model_name="historicalmanga",
            name="last_updated",
        ),
    ]
