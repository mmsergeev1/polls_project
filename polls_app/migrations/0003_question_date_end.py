# Generated by Django 2.2.10 on 2020-10-23 00:41

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0002_auto_20201023_0332'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 30, 0, 41, 24, 580588, tzinfo=utc), verbose_name='Дата окончания'),
        ),
    ]
