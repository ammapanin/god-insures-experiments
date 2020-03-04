# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-07 10:18
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('end_survey', '0002_auto_20190507_1005'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='end_event_donation',
            field=otree.db.models.StringField(choices=[('Yes', 'Yes'), ('No', 'No'), ("I'm not sure", "I'm not sure")], max_length=10000, null=True, verbose_name='Did you make a donation at this event?'),
        ),
    ]
