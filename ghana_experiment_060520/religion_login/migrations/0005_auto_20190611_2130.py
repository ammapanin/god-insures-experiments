# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2019-06-12 01:30
from __future__ import unicode_literals

from django.db import migrations
import otree.db.models


class Migration(migrations.Migration):

    dependencies = [
        ('religion_login', '0004_auto_20190527_0921'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='church',
            field=otree.db.models.StringField(choices=[('The Glory Assemblies of God', 'The Glory Assemblies of God'), ('Agape Assemblies of God', 'Agape Assemblies of God'), ('Crossway Assemblies of God', 'Crossway Assemblies of God'), ('Maranatha Assemblies of God', 'Maranatha Assemblies of God'), ('Central Assemblies of God', 'Central Assemblies of God'), ('Calvary Assemblies of God', 'Calvary Assemblies of God'), ('Grace Assemblies of God', 'Grace Assemblies of God'), ('Other', 'Other')], max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='experiment_date',
            field=otree.db.models.StringField(default='110619', max_length=10000, null=True, verbose_name='Date'),
        ),
        migrations.AlterField(
            model_name='player',
            name='experiment_session',
            field=otree.db.models.StringField(choices=[('Test', 'Test'), ('Individual', 'Individual'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49'), ('50', '50'), ('51', '51'), ('52', '52'), ('53', '53'), ('54', '54'), ('55', '55'), ('56', '56'), ('57', '57'), ('58', '58'), ('59', '59'), ('60', '60'), ('61', '61'), ('62', '62'), ('63', '63'), ('64', '64'), ('65', '65'), ('66', '66'), ('67', '67'), ('68', '68'), ('69', '69'), ('70', '70'), ('71', '71'), ('72', '72'), ('73', '73'), ('74', '74'), ('75', '75'), ('76', '76'), ('77', '77'), ('78', '78'), ('79', '79'), ('80', '80'), ('81', '81'), ('82', '82'), ('83', '83'), ('84', '84'), ('85', '85'), ('86', '86'), ('87', '87'), ('88', '88'), ('89', '89'), ('90', '90'), ('91', '91'), ('92', '92'), ('93', '93'), ('94', '94'), ('95', '95'), ('96', '96'), ('97', '97'), ('98', '98'), ('99', '99'), ('100', '100'), ('101', '101'), ('102', '102'), ('103', '103'), ('104', '104'), ('105', '105'), ('106', '106'), ('107', '107'), ('108', '108'), ('109', '109'), ('110', '110'), ('111', '111'), ('112', '112'), ('113', '113'), ('114', '114'), ('115', '115'), ('116', '116'), ('117', '117'), ('118', '118'), ('119', '119')], max_length=10000, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='experiment_time',
            field=otree.db.models.StringField(default='2130', max_length=10000, null=True, verbose_name='Time'),
        ),
        migrations.AlterField(
            model_name='player',
            name='revival',
            field=otree.db.models.StringField(choices=[('Yes, the person was assigned  and came during the assigned week', 'Yes, the person was assigned  and came during the assigned week'), ('The person was assigned, but did not come during the assigned week.', 'The person was assigned, but did not come during the assigned week.'), ('The person was not assigned to any session this week', 'The person was not assigned to any session this week'), ('The person was assigned to come this week but there was no randomisation', 'The person was assigned to come this week but there was no randomisation')], max_length=10000, null=True, verbose_name='Did this person come to the session where they were assigned?'),
        ),
    ]
