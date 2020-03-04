# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-05-06 07:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import otree.db.models
import otree_save_the_change.mixins


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('otree', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_subsession', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='religion_login_group', to='otree.Session')),
            ],
            options={
                'db_table': 'religion_login_group',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_in_group', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_payoff', otree.db.models.CurrencyField(default=0, null=True)),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('_gbat_arrived', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('_gbat_grouped', otree.db.models.BooleanField(choices=[(True, 'Yes'), (False, 'No')], default=False)),
                ('enumerator', otree.db.models.StringField(choices=[('1 -- Raphael Atta Botchie', '1 -- Raphael Atta Botchie'), ('2 -- Dorcas Sowah', '2 -- Dorcas Sowah'), ('3 -- James Agbeko', '3 -- James Agbeko'), ('4 -- Cyprine Ocloo', '4 -- Cyprine Ocloo'), ('5 -- Sarah Nartey', '5 -- Sarah Nartey'), ('6 -- Iddrisu Abdul Ganiyu', '6 -- Iddrisu Abdul Ganiyu'), ('7 -- Johannes Anaman', '7 -- Johannes Anaman'), ('8 -- Emmanuel Kems', '8 -- Emmanuel Kems'), ('9 -- Kelvin Mintah', '9 -- Kelvin Mintah'), ('10 -- Benjamin Odei', '10 -- Benjamin Odei'), ('11 -- Nana Ama Asiedu', '11 -- Nana Ama Asiedu'), ('12 -- Faustina Bechaiyiri*', '12 -- Faustina Bechaiyiri*'), ('13 -- Sylvester Sadekla*', '13 -- Sylvester Sadekla*'), ('14 -- Amma Panin', '14 -- Amma Panin'), ('15 -- Eva Raiber', '15 -- Eva Raiber'), ('16 -- Julie Lassebie', '16 -- Julie Lassebie')], max_length=10000, null=True)),
                ('treatment', otree.db.models.StringField(choices=[('Insurance', 'Insurance'), ('No insurance', 'No insurance'), ('Insurance information', 'Insurance information')], max_length=10000, null=True)),
                ('experiment_session', otree.db.models.StringField(choices=[('Test', 'Test'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'), ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'), ('56', '56'), ('57', '57'), ('58', '58'), ('59', '59'), ('60', '60'), ('61', '61'), ('62', '62'), ('63', '63'), ('64', '64'), ('65', '65'), ('66', '66'), ('67', '67'), ('68', '68'), ('69', '69'), ('70', '70'), ('71', '71'), ('72', '72'), ('73', '73'), ('74', '74'), ('75', '75'), ('76', '76'), ('77', '77'), ('78', '78'), ('79', '79'), ('80', '80'), ('81', '81'), ('82', '82'), ('83', '83'), ('84', '84'), ('85', '85'), ('86', '86'), ('87', '87'), ('88', '88'), ('89', '89'), ('90', '90')], max_length=10000, null=True)),
                ('church', otree.db.models.StringField(choices=[('The Glory Assemblies of God', 'The Glory Assemblies of God'), ('Agape Assemblies of God', 'Agape Assemblies of God')], max_length=10000, null=True)),
                ('revival', otree.db.models.StringField(choices=[('Revival week', 'Revival week'), ('Regular week', 'Regular week')], max_length=10000, null=True)),
                ('explanation', otree.db.models.StringField(max_length=10000, null=True, verbose_name='Please briefly explain whyyou are not doing the fullexperiment')),
                ('experiment_date', otree.db.models.StringField(default='060519', max_length=10000, null=True, verbose_name='Date')),
                ('experiment_time', otree.db.models.StringField(default='0754', max_length=10000, null=True, verbose_name='Time')),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='religion_login.Group')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='religion_login_player', to='otree.Participant')),
                ('session', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='religion_login_player', to='otree.Session')),
            ],
            options={
                'db_table': 'religion_login_player',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.CreateModel(
            name='Subsession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('round_number', otree.db.models.PositiveIntegerField(db_index=True, null=True)),
                ('session', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='religion_login_subsession', to='otree.Session')),
            ],
            options={
                'db_table': 'religion_login_subsession',
            },
            bases=(otree_save_the_change.mixins.SaveTheChange, models.Model),
        ),
        migrations.AddField(
            model_name='player',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='religion_login.Subsession'),
        ),
        migrations.AddField(
            model_name='group',
            name='subsession',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='religion_login.Subsession'),
        ),
    ]
