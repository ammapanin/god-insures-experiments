# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-06 07:55
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('religion_login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='experiment_time',
            field=otree.db.models.StringField(default='0755', max_length=10000, null=True, verbose_name='Time'),
        ),
    ]
