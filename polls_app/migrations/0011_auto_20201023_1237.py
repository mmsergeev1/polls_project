# Generated by Django 2.2.10 on 2020-10-23 09:37

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0010_auto_20201023_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 10, 30, 9, 37, 24, 541312, tzinfo=utc), verbose_name='Дата окончания'),
        ),
    ]
