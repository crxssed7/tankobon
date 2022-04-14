# Generated by Django 3.2.7 on 2022-04-14 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0014_auto_20220412_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('absolute_number', models.IntegerField(default=-1)),
                ('chapters', models.TextField()),
                ('manga', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.manga')),
            ],
        ),
    ]
