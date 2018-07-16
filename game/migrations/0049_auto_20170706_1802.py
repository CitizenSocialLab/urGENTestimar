# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0048_auto_20170705_2200'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dictator',
            name='data_seleccio2',
        ),
        migrations.RemoveField(
            model_name='dictator',
            name='diners_guanyats2',
        ),
        migrations.RemoveField(
            model_name='dictator',
            name='is_robot2',
        ),
        migrations.RemoveField(
            model_name='dictator',
            name='rival2',
        ),
        migrations.RemoveField(
            model_name='dictator',
            name='rol2',
        ),
        migrations.RemoveField(
            model_name='dictator',
            name='seleccio2',
        ),
    ]
