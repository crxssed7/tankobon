# Generated by Django 3.2.7 on 2022-04-10 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0009_auto_20220410_1740"),
    ]

    operations = [
        migrations.AlterField(
            model_name="chapter",
            name="volume",
            field=models.IntegerField(default=-1),
        ),
        migrations.DeleteModel(
            name="Volume",
        ),
    ]
