# Generated by Django 2.2.16 on 2020-10-27 19:27

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0014_auto_20201023_1238'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 3, 19, 27, 8, 612540, tzinfo=utc), verbose_name='Дата окончания'),
        ),
    ]
