# Generated by Django 3.2.7 on 2022-04-10 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20220410_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='manga',
            name='volume_count',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
