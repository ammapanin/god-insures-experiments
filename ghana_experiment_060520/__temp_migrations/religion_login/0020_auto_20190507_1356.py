# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-07 13:56
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('religion_login', '0019_auto_20190507_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='experiment_time',
            field=otree.db.models.StringField(default='1356', max_length=10000, null=True, verbose_name='Time'),
        ),
    ]
