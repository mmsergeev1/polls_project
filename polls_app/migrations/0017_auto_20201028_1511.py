# Generated by Django 2.2.16 on 2020-10-28 12:11

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls_app', '0016_auto_20201028_1510'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='date_end',
            field=models.DateTimeField(default=datetime.datetime(2020, 11, 4, 12, 11, 50, 608926, tzinfo=utc), verbose_name='Дата окончания'),
        ),
        migrations.AlterField(
            model_name='registeredvote',
            name='anonymous_user_id',
            field=models.IntegerField(blank=True, null=True, verbose_name='Айди анонимного пользователя'),
        ),
    ]
